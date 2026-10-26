"""View-policy regressions independent of a particular identity's proof."""
import unittest
from pathlib import Path
import tempfile
from preprocessing.cache import key_for
from preprocessing.pipeline import prepare
from workflow.engine import prove

class ViewTests(unittest.TestCase):
    def test_cache_separates_views(self):
        identity='FQI-POCHHAMMER-RESIDUES'
        self.assertNotEqual(key_for(identity,view='structured'),key_for(identity,view='expanded'))

    def test_export_policy_and_default(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)
            for view in ('structured','expanded'):
                request=prepare('FQI-POCHHAMMER-RESIDUES',base/view,view=view)
                self.assertEqual(request['policy']['normalization_view'],view)
                source=(base/view/'src/Probe.lean').read_text()
                self.assertEqual('preprocess_export_expanded' in source,view=='expanded')

    def test_unknown_view_rejected(self):
        with self.assertRaisesRegex(ValueError,'unknown_preprocessing_view'):
            prove('FQI-POCHHAMMER-RESIDUES',method='product',preprocess=True,preprocessing_view='method_specific')

if __name__=='__main__':unittest.main()
