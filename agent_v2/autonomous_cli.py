"""Explicit autonomous Train setup and bounded, source-bound resume."""
from dataclasses import asdict, replace
import math
from pathlib import Path
import time

from .models import Artifact, Budget, ContractError, ResidualState, initial_state, digest, thaw
from .storage import IntegrityError, load_train, sha256_file, verify_source

REPOSITORY = Path(__file__).resolve().parents[1]
_SNAPSHOT_KEYS = {'schema_version','config','capabilities','tasks','model_calls','jev_calls',
                  'library','feedback','expansions','repairs','completed_methods'}


def _count(value, name, *, minimum=0, maximum=1000):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ContractError('invalid autonomous '+name)
    return value


def _seconds(value, name):
    if type(value) not in (int,float) or not math.isfinite(value) or not 0 < value <= 86400:
        raise ContractError('invalid autonomous '+name)
    return float(value)


def _path(value, default):
    path = Path(value or default)
    return str((REPOSITORY/path if not path.is_absolute() else path).absolute())


def _config(args):
    from .autonomous import default_config
    from .model_client import ModelConfig, _credential, _endpoint
    from .jev_client import JevConfig
    config = default_config()
    config.update(action_seconds=_seconds(args.action_seconds,'action_seconds'),
        max_model_calls=_count(args.max_model_calls,'max_model_calls',minimum=1),
        max_expansions=_count(args.max_expansions,'max_expansions'),
        max_repairs=_count(args.max_repairs,'max_repairs'),selector=args.selector)
    if args.selector not in ('rule','jev'):
        raise ContractError('invalid autonomous selector')
    model_config = ModelConfig(model=args.model or 'gpt-6-astra',
        endpoint=args.model_endpoint or None, credential_path=_path(args.model_credential,'API_GPT'),
        max_calls=config['max_model_calls'],reasoning_effort='high')
    effective_endpoint = model_config.endpoint
    if effective_endpoint is None:
        _,effective_endpoint = _credential(model_config)
    model_config = replace(model_config,endpoint=_endpoint(effective_endpoint,'https://api.openai.com','responses'))
    config['model'] = asdict(model_config)
    config['jev'] = asdict(JevConfig(credential_path=_path(args.jev_credential,'API_Jev'),
        max_calls=_count(args.max_steps,'max_steps',minimum=1)))
    return config


def _dependencies(*groups):
    result = {}
    for group in groups:
        for artifact in group:
            if not isinstance(artifact,Artifact):
                artifact = Artifact.from_dict(artifact)
            if artifact.path in result and result[artifact.path] != artifact:
                raise IntegrityError('dependency changed during autonomous setup')
            result[artifact.path] = artifact
    return tuple(result[path] for path in sorted(result))


def _artifact(path):
    return Artifact(str(path),sha256_file(path))


def _library_dependencies(records):
    from .library import _FOUNDATIONS
    fixed = [REPOSITORY/path for _,path in _FOUNDATIONS]
    fixed += [REPOSITORY/'project'/name for name in ('lake-manifest.json','lean-toolchain','lakefile.toml')]
    artifacts = [_artifact(path) for path in fixed]
    for record in records:
        provenance = record.get('provenance') if isinstance(record,dict) else None
        if (not isinstance(provenance,dict) or not isinstance(provenance.get('path'),str) or
                not isinstance(provenance.get('sha256'),str)):
            raise IntegrityError('library declaration has no bound provenance')
        path = Path(provenance['path'])
        current = _artifact(path)
        if current.sha256 != provenance['sha256']:
            raise IntegrityError('library declaration source changed during lookup')
        artifacts.append(current)
        if record.get('lean_binary'):
            artifacts.append(_artifact(Path(record['lean_binary'])))
    return _dependencies(artifacts)


def _unsupported(store,source,args,started,reason,diagnostics=()):
    from .graph import Graph
    from .loop import finish
    state,representation=initial_state(source,Budget(args.seconds,args.max_steps))
    graph=Graph(source.sha256); graph.add_node(representation)
    budget=state.b.charge(time.monotonic()-started,0)
    status='budget_exhausted' if reason=='setup_budget_exhausted' or budget.seconds<=0 else 'incomplete'
    state=replace(state,b=budget,status=status)
    store.write_json('initial_state.json',state.to_dict())
    return finish(store,state,graph,reason,diagnostics).status


def _clients(config,store,*,model_calls=0,jev_calls=0):
    from .model_client import make_model_client
    from .jev_client import JevSelector
    model=make_model_client(config['model'],calls_used=model_calls)
    jev=(JevSelector(config['jev'],attempt_root=store.path('selection_calls'),calls_used=jev_calls)
         if config['selector']=='jev' else None)
    return model,jev


def train_run(args,base_store):
    from .autonomous import AutonomousRuntime,AutonomousStore,run
    from .cli import runtime_dependencies
    from .graph import Graph
    from .graph_builder import sync_residual_graph
    from .library import LocalLibrary,LibraryUnavailable
    from .local_proof_checker import LocalLeanChecker
    from .method_registry import builtin_registry,resolve
    started=time.monotonic()
    _seconds(args.seconds,'seconds'); _count(args.max_steps,'max_steps',minimum=1)
    config=_config(args)
    registry=builtin_registry()
    methods=list(registry.ids()) if args.methods=='all' else args.methods.split(',')
    if not methods or len(set(methods))!=len(methods) or any(method not in registry.ids() for method in methods):
        raise ContractError('invalid or duplicate autonomous methods')
    source=load_train(args.identity,base_store,REPOSITORY)
    source=replace(source,dependencies=_dependencies(source.dependencies,runtime_dependencies()))
    inventory={}; applicable={}; propositions=set()
    for method in methods:
        spec=registry.get(method)
        if spec.capability_level=='L0':
            inventory[method]={'status':'not_applicable','reason':'capability_unavailable'}
            continue
        try:
            result=resolve(spec.frontend)(source.to_dict(),run_root=base_store.root)
        except (IntegrityError,ContractError):
            raise
        except Exception as error:
            # Source frontends never contain credentials; retain a local type
            # rather than arbitrary exception text in setup evidence.
            result={'status':'frontend_error','error_type':type(error).__name__}
        if not isinstance(result,dict) or not isinstance(result.get('status'),str):
            raise ContractError('invalid autonomous frontend result')
        inventory[method]=result
        if result['status']=='applicable':
            proposition=result.get('original_proposition')
            if not isinstance(proposition,str) or not proposition.strip():
                inventory[method]=dict(result,status='unsupported',reason='missing_closed_original')
                continue
            propositions.add(proposition); applicable[method]=(spec,result)
    base_store.write_json('frontend_inventory.json',{'schema_version':1,'source_sha256':source.sha256,
        'methods':inventory,'selected_methods':methods})
    if len(propositions)!=1:
        return _unsupported(base_store,source,args,started,'unsupported_original_proposition',
                            [{'code':'no_unique_closed_original','count':len(propositions)}])
    source=replace(source,proposition=next(iter(propositions)))
    capabilities={}
    groups=[source.dependencies]
    for method,(spec,result) in applicable.items():
        groups.append(tuple(resolve(spec.dependency_provider)()))
        capabilities[method]={'status':'applicable','version':spec.version,'family':spec.family,
            'supported_structures':list(spec.supported_structures),'limitations':list(spec.limitations),
            'local_lean':spec.local_lean,'local_proposition':result.get('local_proposition'),
            'estimated_seconds':spec.estimated_seconds}
    source=replace(source,dependencies=_dependencies(*groups))
    checker=LocalLeanChecker(REPOSITORY)
    try:
        checker._bound(source,base_store.root)
    except IntegrityError as error:
        if str(error)!='Source has no implemented formal original translation':
            raise
        return _unsupported(base_store,source,args,started,'formal_source_translation_unavailable',
                            [{'code':'unsupported_formal_source'}])
    remaining=args.seconds-(time.monotonic()-started)
    if remaining<=0:
        return _unsupported(base_store,source,args,started,'setup_budget_exhausted')
    try:
        library=LocalLibrary(REPOSITORY,seconds=min(30.,remaining)).query('',limit=32)
    except LibraryUnavailable as error:
        base_store.write_json('library_error.json',{'code':str(error)})
        # Missing retrieval is an environment failure, never an empty-library
        # fallback silently described as successful lookup.
        from .graph import Graph
        from .loop import finish
        state,representation=initial_state(source,Budget(args.seconds,args.max_steps))
        graph=Graph(source.sha256);graph.add_node(representation)
        budget=state.b.charge(time.monotonic()-started,0)
        exhausted=budget.seconds<=0
        state=replace(state,b=budget,status='budget_exhausted' if exhausted else 'environment_blocked')
        base_store.write_json('initial_state.json',state.to_dict())
        return finish(base_store,state,graph,'setup_budget_exhausted' if exhausted else 'library_unavailable',
                      [{'code':str(error)}]).status
    source=replace(source,dependencies=_dependencies(source.dependencies,_library_dependencies(library)))
    library_file=base_store.write_json('library_inventory.json',{'schema_version':1,'declarations':library})
    config_file=base_store.write_json('autonomous_config.json',{'schema_version':1,'config':config,
        'capabilities':capabilities,'library_sha256':sha256_file(library_file)})
    source=replace(source,dependencies=_dependencies(source.dependencies,(_artifact(config_file),_artifact(library_file))))
    # Recheck each source capability against the now frozen complete context.
    for method,(spec,_) in applicable.items():
        current=resolve(spec.frontend)(source.to_dict(),run_root=base_store.root)
        if current.get('status')!='applicable' or current.get('original_proposition')!=source.proposition:
            raise IntegrityError('frontend changed after autonomous source freeze')
    verify_source(source,base_store.root)
    state,representation=initial_state(source,Budget(args.seconds,args.max_steps))
    graph=Graph(source.sha256);graph.add_node(representation)
    sync_residual_graph(state,graph,capabilities,seconds=config['action_seconds'])
    model,jev=_clients(config,base_store)
    runtime=AutonomousRuntime(config,capabilities,model,checker,library,jev=jev)
    store=AutonomousStore(base_store.root,runtime)
    state=replace(state,b=state.b.charge(time.monotonic()-started,0))
    store.write_json('initial_state.json',state.to_dict())
    return run(state,graph,store,pause_after=getattr(args,'pause_after',None)).status


def _saved_metadata(base_store,snapshot,state):
    from .autonomous import default_config
    from .model_client import ModelConfig
    from .jev_client import JevConfig
    if not isinstance(snapshot,dict) or set(snapshot)!=_SNAPSHOT_KEYS or type(snapshot['schema_version']) is not int or snapshot['schema_version']!=1:
        raise IntegrityError('invalid autonomous snapshot schema')
    config=snapshot['config']
    if not isinstance(config,dict) or set(config)!=set(default_config()):
        raise IntegrityError('invalid autonomous config schema')
    _seconds(config['action_seconds'],'action_seconds')
    _count(config['max_model_calls'],'max_model_calls',minimum=1)
    for key in ('max_expansions','max_repairs'):
        _count(config[key],key)
    if config['selector'] not in ('rule','jev'):
        raise IntegrityError('invalid autonomous selector')
    model_config=ModelConfig(**config['model']);jev_config=JevConfig(**config['jev'])
    if model_config.max_calls!=config['max_model_calls']:
        raise IntegrityError('model call limits differ')
    _count(snapshot['model_calls'],'model_calls',maximum=model_config.max_calls)
    _count(snapshot['jev_calls'],'jev_calls',maximum=jev_config.max_calls)
    _count(snapshot['expansions'],'expansions',maximum=config['max_expansions'])
    _count(snapshot['repairs'],'repairs',maximum=config['max_repairs'])
    if config['selector']=='rule' and snapshot['jev_calls']!=0:
        raise IntegrityError('rule selection cannot have Jev calls')
    metadata=base_store.read_json('autonomous_config.json')
    if (not isinstance(metadata,dict) or set(metadata)!={'schema_version','config','capabilities','library_sha256'} or
            metadata['schema_version']!=1 or metadata['config']!=config or metadata['capabilities']!=snapshot['capabilities']):
        raise IntegrityError('autonomous provider/capability configuration changed')
    frozen={artifact.path:artifact.sha256 for artifact in state.G.dependencies}
    for filename in ('autonomous_config.json','library_inventory.json'):
        file=base_store.path(filename)
        if frozen.get(str(file))!=sha256_file(file):
            raise IntegrityError('autonomous metadata is not frozen to original source')
    library=base_store.read_json('library_inventory.json')
    if (set(library)!={'schema_version','declarations'} or library['schema_version']!=1 or
            library['declarations']!=snapshot['library'] or
            sha256_file(base_store.path('library_inventory.json'))!=metadata['library_sha256']):
        raise IntegrityError('autonomous library changed')
    if not isinstance(snapshot['tasks'],list) or len(snapshot['tasks'])>1000 or not isinstance(snapshot['feedback'],list) or len(snapshot['feedback'])>3:
        raise IntegrityError('invalid autonomous task or feedback inventory')
    if not isinstance(snapshot['completed_methods'],dict):
        raise IntegrityError('invalid completed method inventory')
    certs={certificate.id for certificate in state.C}
    for method,ids in snapshot['completed_methods'].items():
        if method not in snapshot['capabilities'] or not isinstance(ids,list) or not ids or len(set(ids))!=len(ids) or any(i not in certs for i in ids):
            raise IntegrityError('completed method has no current checked certificates')
    return config


def resume_run(args,base_store):
    from .autonomous import AutonomousRuntime,AutonomousStore,run
    from .local_tasks import LocalTask
    from .local_proof_checker import LocalLeanChecker
    from .loop import resume
    saved=base_store.load_checkpoint()
    if 'autonomous' not in saved:
        raise IntegrityError('autonomous checkpoint metadata missing')
    snapshot=saved['autonomous']
    state=ResidualState.from_dict(saved['state'])
    config=_saved_metadata(base_store,snapshot,state)
    # Resume has no route to replace saved provider settings using parser defaults.
    for key,expected in (('model',config['model']['model']),('model_endpoint',config['model']['endpoint']),
                         ('selector',config['selector'])):
        given=getattr(args,key,None)
        if given is not None and given!=expected:
            raise IntegrityError('resume cannot change autonomous provider configuration')
    tasks=tuple(LocalTask.from_dict(task) for task in snapshot['tasks'])
    if len({task.id for task in tasks})!=len(tasks) or any(task.source!=state.G for task in tasks):
        raise IntegrityError('autonomous task original source differs')
    checker=LocalLeanChecker(REPOSITORY,tasks=tasks)
    model,jev=_clients(config,base_store,model_calls=snapshot['model_calls'],jev_calls=snapshot['jev_calls'])
    runtime=AutonomousRuntime(config,snapshot['capabilities'],model,checker,snapshot['library'],jev=jev)
    runtime.expansions=snapshot['expansions'];runtime.repairs=snapshot['repairs']
    runtime.completed_methods=snapshot['completed_methods']
    runtime.executor.feedback=snapshot['feedback']
    store=AutonomousStore(base_store.root,runtime)
    state,graph=resume(store,checker)
    return run(state,graph,store,pause_after=getattr(args,'pause_after',None)).status
