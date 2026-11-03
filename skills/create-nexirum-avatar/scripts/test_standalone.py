"""Offline integration test using only an isolated skill and synthetic fixtures.

Requires the normal packing dependencies, including ImageMagick. This exercises
plan/pack/check, not image generation, artistic quality, or Nexirum app runtime.
"""

import base64
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

from PIL import Image, ImageDraw


SKILL = Path(__file__).resolve().parents[1]
PACKING_AVAILABLE = bool(
    (shutil.which('magick') or (shutil.which('convert') and shutil.which('montage')))
    and importlib.util.find_spec('numpy') and importlib.util.find_spec('scipy')
)
STATES = ['idle', 'thinking', 'listening', 'talking', 'happy', 'warning', 'sleep',
          'error', 'success', 'wake', 'hello', 'confused', 'searching', 'working']


@unittest.skipUnless(PACKING_AVAILABLE, 'Install packing dependencies to run standalone integration.')
class StandaloneSkillTests(unittest.TestCase):
    def test_only_skill_folder_can_plan_pack_and_validate_a_complete_delivery(self):
        with tempfile.TemporaryDirectory(prefix='avatar-standalone-') as temporary:
            root = Path(temporary)
            installed = root/'installed skill'
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            workspace = root/'new workspace'
            workspace.mkdir()
            script = installed/'scripts/avatar_tool.py'
            self.assertFalse((root/'examples').exists())
            self.assertEqual(list(workspace.iterdir()), [])

            def run(*args):
                completed = subprocess.run(
                    [sys.executable, '-E', '-B', str(script), *map(str, args)],
                    cwd=workspace, capture_output=True, text=True, encoding='utf-8',
                    errors='replace', timeout=600)
                self.assertEqual(completed.returncode, 0, completed.stdout+'\n'+completed.stderr)
                return json.loads(completed.stdout)

            # Procedural test fixtures, not mascot artwork or a delivered example.
            # White and black opaque details plus a detached marker exercise alpha
            # preservation and component grouping. Each frame has a different eye.
            for sheet in range(2):
                image = Image.new('RGBA', (1280,1120))
                draw = ImageDraw.Draw(image)
                for row in range(7):
                    for col in range(10):
                        x,y = col*128,row*160
                        draw.rectangle((x+44,y+45,x+84,y+105), fill=(50+sheet*90,90+row*15,150,255))
                        draw.rectangle((x+49,y+50,x+79,y+70), fill=(0,0,0,255))
                        draw.rectangle((x+54+col,y+56,x+57+col,y+60), fill=(255,255,255,255))
                        draw.rectangle((x+50,y+106,x+58,y+128), fill=(25,25,25,255))
                        draw.rectangle((x+70,y+106,x+78,y+128), fill=(25,25,25,255))
                        draw.rectangle((x+92,y+25,x+97,y+30), fill=(240,80,30,255))
                if sheet == 1:
                    image = image.quantize(colors=32, method=Image.Quantize.FASTOCTREE)
                image.save(workspace/f'sheet-{sheet+1}.png')
            with Image.open(workspace/'sheet-2.png') as indexed:
                self.assertEqual(indexed.mode, 'P')
                self.assertIn('transparency', indexed.info)

            plan_path = workspace/'plan.json'
            proposal = run('plan', '--id', 'fresh-avatar', '--name', 'Fresh avatar',
                           '--sheet', workspace/'sheet-1.png', '--rows', ','.join(STATES[:7]),
                           '--sheet', workspace/'sheet-2.png', '--rows', ','.join(STATES[7:]),
                           '--out', plan_path)
            self.assertFalse(proposal['reviewed'])
            plan = json.loads(plan_path.read_text(encoding='utf-8'))
            self.assertEqual([s for sheet in plan['sheets'] for s in sheet['states']], STATES)
            # Geometry is known exactly because this test constructed the fixtures.
            plan['reviewed'] = True
            plan_path.write_text(json.dumps(plan), encoding='utf-8')
            self.assertFalse((workspace/'animations.json').exists())
            original_preset = (installed/'assets/animations.json').read_bytes()

            delivery = workspace/'delivery'
            packed = run('pack', plan_path, '--out', delivery)
            self.assertEqual(packed['frames'], 140)
            report = run('check', delivery/'fresh-avatar')
            self.assertTrue(report['compatible'])
            self.assertEqual(report['frame_count'], 140)
            self.assertEqual(report['warnings'], [])
            self.assertTrue(report['visual_review_required'])
            self.assertFalse(report['app_runtime_tested'])

            expected = json.loads(original_preset)
            expected['name'] = 'Fresh avatar'
            catalog = json.loads((delivery/'fresh-avatar/animations.json').read_text(encoding='utf-8'))
            self.assertEqual(catalog, expected)
            self.assertEqual((installed/'assets/animations.json').read_bytes(), original_preset)
            preview = (delivery/'preview.html').read_text(encoding='utf-8')
            self.assertNotIn('__AVATAR_DATA__', preview)
            self.assertNotIn(str(root), preview)
            for number in (1,2):
                with Image.open(delivery/f'contact-{number}.png') as contact:
                    self.assertGreater(contact.width, 0)
                    self.assertGreater(contact.height, 0)
            with zipfile.ZipFile(delivery/'fresh-avatar.zip') as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(json.loads(archive.read('fresh-avatar/animations.json')), expected)
                self.assertEqual(archive.read('preview.html'), (delivery/'preview.html').read_bytes())
                for state in STATES:
                    filename = catalog['states'][state]['atlas']
                    path = delivery/'fresh-avatar'/filename
                    blob = path.read_bytes()
                    self.assertEqual(archive.read('fresh-avatar/'+filename), blob)
                    self.assertIn(base64.b64encode(blob).decode('ascii'), preview)
                    with Image.open(path) as atlas:
                        self.assertEqual(atlas.size, (2560,256))
                        frames = [atlas.crop((i*256,0,(i+1)*256,256)) for i in range(10)]
                        self.assertEqual(len({frame.tobytes() for frame in frames}), 10)
                        for frame in frames:
                            colours = {colour for _,colour in frame.getcolors(maxcolors=256*256)}
                            self.assertIn((0,0,0,255), colours)
                            self.assertIn((255,255,255,255), colours)
                            self.assertIn((240,80,30,255), colours)
                            self.assertTrue(any(colour[3] == 0 for colour in colours))


if __name__ == '__main__':
    unittest.main(verbosity=2)
