"""Offline regression checks for package boundaries; no generated artwork or APIs."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location('avatar_tool', Path(__file__).with_name('avatar_tool.py'))
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class AvatarFormatTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.catalog = tool.preset()
        atlas = Image.new('RGBA', (2560,256))
        draw = ImageDraw.Draw(atlas)
        for frame in range(10):
            draw.rectangle((frame*256+80,90,frame*256+170,238), fill=(40,80,150,255))
        for item in self.catalog['states'].values():
            atlas.save(self.root/item['atlas'], lossless=True)
        self.save()

    def tearDown(self):
        self.temporary.cleanup()

    def save(self):
        tool.write_json(self.root/'animations.json', self.catalog)

    def report(self):
        return tool.inspect_avatar(self.root)[0]

    def test_complete_preset_passes(self):
        result = self.report()
        self.assertTrue(result['compatible'])
        self.assertEqual(result['frame_count'],140)
        self.assertTrue(result['visual_review_required'])
        self.assertFalse(result['app_runtime_tested'])

    def test_oversize_is_rejected_before_decode(self):
        (self.root/'idle-atlas.webp').write_bytes(b'x'*(tool.LIMIT+1))
        result = self.report()
        self.assertFalse(result['compatible'])
        self.assertIn('224 KiB',result['errors'][0])

    def test_path_traversal_and_symlink_are_rejected(self):
        self.catalog['states']['idle']['atlas']='../outside.webp'; self.save()
        self.assertFalse(self.report()['compatible'])
        self.catalog['states']['idle']['atlas']='idle-atlas.webp'; self.save()
        path = self.root/'idle-atlas.webp'; path.unlink()
        path.symlink_to(self.root/'thinking-atlas.webp')
        self.assertFalse(self.report()['compatible'])

    def test_missing_state_and_missing_file_are_rejected(self):
        saved = self.catalog['states'].pop('sleep'); self.save()
        self.assertFalse(self.report()['compatible'])
        self.catalog['states']['sleep']=saved; self.save()
        (self.root/'sleep-atlas.webp').unlink()
        self.assertFalse(self.report()['compatible'])

    def test_dimensions_and_static_encoding(self):
        path = self.root/'idle-atlas.webp'
        Image.new('RGBA',(256,256),(0,0,0,0)).save(path,lossless=True)
        self.assertFalse(self.report()['compatible'])
        first=Image.new('RGBA',(2560,256),(10,20,30,255))
        second=Image.new('RGBA',(2560,256),(30,20,10,255))
        first.save(path,save_all=True,append_images=[second],duration=80,loop=0,lossless=True)
        self.assertFalse(self.report()['compatible'])

    def test_empty_and_opaque_frames_are_rejected(self):
        for colour in [(0,0,0,0),(0,0,0,255)]:
            Image.new('RGBA',(2560,256),colour).save(self.root/'idle-atlas.webp',lossless=True)
            self.assertFalse(self.report()['compatible'])

    def test_duplicate_json_and_changed_timing_are_rejected(self):
        path=self.root/'animations.json'
        path.write_text('{"name":"one","name":"two"}')
        self.assertFalse(self.report()['compatible'])
        self.catalog['states']['idle']['ms']=1; self.save()
        self.assertFalse(self.report()['compatible'])

    def test_unreviewed_plan_cannot_be_packed(self):
        path=self.root/'plan.json'
        tool.write_json(path,{'avatar_id':'demo','reviewed':False})
        with self.assertRaisesRegex(ValueError,'reviewed=true'):
            tool.pack_plan(path,self.root/'delivery')
        self.assertFalse((self.root/'delivery').exists())

    def test_script_text_is_escaped_in_preview(self):
        result,catalog,blobs=tool.inspect_avatar(self.root)
        catalog['name']='</script><script>alert(1)</script>'
        html=tool.render_preview(catalog,blobs)
        self.assertNotIn(catalog['name'],html)
        start=html.index('const avatar=')+len('const avatar=')
        end=html.index(';\nconst labels=',start)
        self.assertEqual(json.loads(html[start:end])['name'],catalog['name'])

    def test_unsafe_folder_names_and_overwrites_are_rejected(self):
        for value in ['../escape','CON','con','lpt1','two words','cão','-bad','a--b']:
            with self.assertRaises(ValueError):tool.avatar_id(value)
        with self.assertRaisesRegex(ValueError,'Output exists'):
            tool.package_avatar(self.root,'demo',self.root)


if __name__=='__main__':
    unittest.main()
