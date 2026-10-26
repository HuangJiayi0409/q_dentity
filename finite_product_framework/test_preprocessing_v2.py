"""Storage fidelity, integrity and simultaneous method-request regressions."""
from concurrent.futures import ThreadPoolExecutor
import copy
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from preprocessing.wire import pack, unpack
from preprocessing import cache


class WireTests(unittest.TestCase):
    def test_lossless_and_sharing(self):
        child = {'tag':'bvar','index':0}
        value = {'a':[child]*100, 'b':child, 'scalar':[True,False,None,1,1.0,'中文']}
        packet = pack(value)
        decoded = unpack(json.loads(json.dumps(packet)))
        self.assertEqual(decoded, value)
        self.assertIs(decoded['a'][0], decoded['b'])
        self.assertLess(len(json.dumps(packet)),len(json.dumps(value)))

    def test_bad_references(self):
        for ref in (-1, 0, True, '0'):
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                unpack({'packet_version':2,'nodes':[{'child':{'$ref':ref}}],'root':{'$ref':0}})

    def test_unknown_packet_and_legacy(self):
        with self.assertRaises(ValueError): unpack({'packet_version':3})
        self.assertEqual(unpack({'wire_version':1}),{'wire_version':1})


class CacheTests(unittest.TestCase):
    def test_concurrent_publish_and_corruption(self):
        calls=[]
        def fake_run(identity, directory, **kwargs):
            calls.append(identity)
            directory.mkdir()
            time.sleep(.1)
            (directory/'request.json').write_text('{}')
            (directory/'status.json').write_text('{"status":"verified_unchanged"}')
            (directory/'bundle.json').write_text('{"checked":true}')
            return {'status':'verified_unchanged'}
        with tempfile.TemporaryDirectory() as root, \
                patch.object(cache,'key_for',return_value='fixed-key'), \
                patch.object(cache,'run',side_effect=fake_run), \
                patch.object(cache,'check_snapshot'):
            with ThreadPoolExecutor(max_workers=3) as workers:
                rows=list(workers.map(lambda _: cache.cached_run('id',root=root),range(3)))
            self.assertEqual(calls,['id'])
            self.assertEqual(sum(not s['cache_hit'] for _,s in rows),1)
            self.assertEqual(len({str(p) for p,_ in rows}),1)
            (rows[0][0]/'bundle.json').write_text('tampered')
            with self.assertRaisesRegex(ValueError,'cache_artifact_changed'):
                cache.cached_run('id',root=root)

    def test_failed_construction_never_published(self):
        with tempfile.TemporaryDirectory() as root, \
                patch.object(cache,'key_for',return_value='fixed-key'), \
                patch.object(cache,'run',side_effect=ValueError('failed')):
            with self.assertRaises(ValueError): cache.cached_run('id',root=root)
            self.assertFalse((Path(root)/'fixed-key').exists())


if __name__=='__main__': unittest.main()
