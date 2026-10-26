"""Independent boundaries of the portable installation interface."""
import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import offtake

class InstallationGuards(unittest.TestCase):
 def setUp(self):
  scratch=ROOT.parent/'test-work';scratch.mkdir(exist_ok=True)
  self.tmp=tempfile.TemporaryDirectory(dir=scratch)
  self.folder=Path(self.tmp.name)
  self.patch=patch.object(offtake,'ROOT',self.folder);self.patch.start()
 def tearDown(self):self.patch.stop();self.tmp.cleanup()
 def manifest(self,path='engine/module.py',payload=b'# fixture'):
  target=self.folder/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(payload)
  row={'path':path,'sha256':hashlib.sha256(payload).hexdigest()}
  (self.folder/'DISTRIBUTION_MANIFEST.json').write_text(json.dumps({'immutable_files':[row]}))
  return target
 def test_valid_manifest_reads_without_writes(self):
  f=self.manifest();before=f.read_bytes();self.assertTrue(offtake.verify_distribution()['passed']);self.assertEqual(before,f.read_bytes())
 def test_missing_manifest_blocks(self):
  with self.assertRaisesRegex(ValueError,'manifest is missing'):offtake.verify_distribution()
 def test_missing_program_blocks(self):
  f=self.manifest();f.unlink()
  with self.assertRaisesRegex(ValueError,'changed or missing'):offtake.verify_distribution()
 def test_modified_program_blocks(self):
  f=self.manifest();f.write_bytes(b'# changed')
  with self.assertRaisesRegex(ValueError,'changed or missing'):offtake.verify_distribution()
 def test_parent_traversal_blocks(self):
  with self.assertRaises(ValueError):offtake.private_path('../outside')
 def test_absolute_outside_path_blocks(self):
  with self.assertRaises(ValueError):offtake.private_path(str(self.folder.parent/'other'))
 def test_installation_root_not_file(self):
  with self.assertRaises(ValueError):offtake.private_path('.')
 def test_missing_company_configuration_cannot_be_inferred(self):
  self.manifest()
  with self.assertRaises((ValueError,FileNotFoundError)):offtake.configure()
 def test_cache_invalidates_when_portable_stage_changes(self):
  sys.path.insert(0,str(ROOT/'automation'))
  import run_monthly
  engine=self.folder/'engine';engine.mkdir()
  automation=self.folder/'automation';automation.mkdir()
  stage=self.folder/'portable_stage.py';stage.write_text('# version one')
  with patch.object(run_monthly,'ROOT',self.folder),patch.object(run_monthly,'ENGINE',engine),patch.object(run_monthly,'HERE',automation):
   first=run_monthly.fingerprint('2026-10',{},{});stage.write_text('# version two')
   self.assertNotEqual(first,run_monthly.fingerprint('2026-10',{},{}))

if __name__=='__main__':unittest.main(verbosity=2)
