"""Catalogue-driven extension of the shared P1/product expression serializer.

The serializer only accepts fully applied registered objects. Mathematical
interpretation stays in solver-readable rules; emitted Lean still checks source
equivalence. This is not a second theorem-proving pipeline.
"""
from .catalog import ENTRY_UNFOLDS
from .registry import Library, LibraryError


def extractor_text(original):
    lib=Library()
    marker='  if let .const name _ := e.getAppFn then'
    if original.count(marker)!=1:raise LibraryError('extractor_template_changed')
    # Full argument counts are checked, including the explicit type/instance prefix.
    lines=['  if let .const libraryName _ := e.getAppFn then']
    for symbol,obj in lib.objects.items():
        arity=len(obj['arguments']);total=arity+obj['implicit_prefix']
        lines += [f'    if libraryName.toString == "{symbol}" then',
                  f'      unless args.size == {total} do throwError "MATH_LIBRARY_PARTIAL_APPLICATION: {{e}}"',
                  '      return node libraryName.toString #['+', '.join(
                      '← expressionJSON args['+str(i)+']!' for i in range(obj['implicit_prefix'],total))+']']
    lines.append(marker)
    return original.replace(marker,'\n'.join(lines))


def query_trace(raw):
    lib=Library();found=set();symbols=set(lib.objects)
    def visit(node):
        if node.get('op') in symbols:found.add(node['op'])
        for arg in node.get('args',[]):visit(arg)
        if 'body' in node:visit(node['body'])
    visit(raw)
    return dict(catalog_sha256=lib.sha256,objects=[lib.lookup(s) for s in sorted(found)],
                original_proof_established=False)


def entry_views(raw):
    """Expand only opted-in source wrappers; preserve established old routes."""
    from .source_views import finite_sum_view
    lib=Library();trace=[]
    def visit(tree):
        matches=lib.lookup(tree['op'],'finite_sum')['rules']
        if any(r['id'] in ENTRY_UNFOLDS for r in matches):
            view=finite_sum_view(tree,library=lib)
            trace.extend(view['library_trace'])
            return view['expression']
        out=dict(tree)
        if 'args' in out:out['args']=[visit(x) for x in out['args']]
        if 'body' in out:out['body']=visit(out['body'])
        return out
    result=visit(raw)
    return result,trace
