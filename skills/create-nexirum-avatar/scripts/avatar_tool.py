#!/usr/bin/env python3
"""Validate, pack, and preview Nexirum avatars without network/model calls."""

import argparse
import base64
import hashlib
import io
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
LIMIT = 224 * 1024
CELL = 256
FRAMES = 10
Image.MAX_IMAGE_PIXELS = 25_000_000


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)


def preset():
    return read_json(SKILL / 'assets/animations.json')


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def avatar_id(value):
    devices = {'con', 'prn', 'aux', 'nul'} | {f'{p}{n}' for p in ('com', 'lpt') for n in range(1, 10)}
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value) or len(value) > 64 or value in devices:
        raise ValueError('Use a safe lowercase ASCII ID with single hyphens; avoid Windows device names.')
    return value


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{label} must be a finite number')
    return value


def im_command(mode='convert'):
    executable = shutil.which('magick')
    if executable:
        return [executable] if mode == 'convert' else [executable, mode]
    executable = shutil.which(mode)
    if not executable:
        raise ValueError('ImageMagick is required for packing and contact sheets.')
    return [executable]


def run_image(args, mode='convert'):
    result = subprocess.run(im_command(mode) + [str(x) for x in args], capture_output=True, text=True)
    if result.returncode:
        raise ValueError('ImageMagick failed: ' + result.stderr[-1500:])


def inspect_avatar(folder):
    """Validate the complete supplied preset; return captured bytes for packaging."""
    folder = Path(folder).resolve()
    report = {'compatible': False, 'errors': [], 'warnings': [], 'states': {},
              'visual_review_required': True, 'app_runtime_tested': False}
    blobs = {}
    catalog = None
    try:
        catalog = read_json(folder / 'animations.json')
        if not isinstance(catalog, dict) or not isinstance(catalog.get('name'), str) or not catalog['name'].strip():
            raise ValueError('A nonempty display name is required.')
        if type(catalog.get('version')) is not int or catalog['version'] != 1:
            raise ValueError('Expected preset version 1.')
        expected = preset()['states']
        states = catalog.get('states')
        if not isinstance(states, dict) or set(states) != set(expected):
            raise ValueError('Expected all 14 preset states, without extra or missing states.')
        used = set()
        for state, spec in expected.items():
            item = states[state]
            if not isinstance(item, dict) or set(item) != set(spec):
                raise ValueError(f'{state}: unexpected state fields')
            for key in ('frames', 'ms', 'loop', 'nextState'):
                if key in spec and (type(item.get(key)) is not type(spec[key]) or item[key] != spec[key]):
                    raise ValueError(f'{state}: preserve preset {key}={spec[key]}')
            name = item['atlas']
            if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*\.webp', name):
                raise ValueError(f'{state}: atlas must be a safe local WebP basename')
            path = folder / name
            if path.is_symlink() or path.resolve().parent != folder or name in used:
                raise ValueError(f'{state}: duplicated or unsafe atlas reference')
            used.add(name)
            if path.stat().st_size > LIMIT:
                raise ValueError(f'{state}: exceeds 224 KiB ({path.stat().st_size} bytes)')
            data = path.read_bytes()
            with Image.open(io.BytesIO(data)) as im:
                im.load()
                if im.format != 'WEBP' or getattr(im, 'is_animated', False):
                    raise ValueError(f'{state}: expected static WebP')
                if im.size != (FRAMES * CELL, CELL) or 'A' not in im.getbands():
                    raise ValueError(f'{state}: expected 2560x256 with alpha')
                alpha = im.getchannel('A')
                frames = []
                for index in range(FRAMES):
                    cell = alpha.crop((index * CELL, 0, (index + 1) * CELL, CELL))
                    hist = cell.histogram()
                    bbox = cell.getbbox()
                    if hist[0] == 0 or sum(hist[240:]) < 64 or bbox is None:
                        raise ValueError(f'{state}:{index}: empty, nearly invisible, or no transparent background')
                    if bbox[0] == 0 or bbox[1] == 0 or bbox[2] == CELL or bbox[3] == CELL:
                        report['warnings'].append(f'{state}:{index}: content touches a cell edge; inspect clipping')
                    frames.append({'bbox': list(bbox), 'transparent_pixels': hist[0],
                                   'near_opaque_pixels': sum(hist[240:])})
            blobs[name] = data
            report['states'][state] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'frames': frames}
        report['compatible'] = True
        report['frame_count'] = FRAMES * len(expected)
    except (OSError, ValueError, TypeError, KeyError, Image.DecompressionBombError) as exc:
        report['errors'].append(str(exc))
    return report, catalog, blobs


def render_preview(catalog, blobs):
    payload = {'name': catalog['name'], 'states': {}}
    for state, item in catalog['states'].items():
        payload['states'][state] = dict(item, image='data:image/webp;base64,' + base64.b64encode(blobs[item['atlas']]).decode('ascii'))
    encoded = json.dumps(payload, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    encoded = encoded.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return (SKILL / 'assets/preview.html').read_text(encoding='utf-8').replace('__AVATAR_DATA__', encoded)


def contact_sheets(catalog, report, avatar_dir, stage, work):
    boxes = [frame['bbox'] for state in report['states'].values() for frame in state['frames']]
    left = max(0, min(b[0] for b in boxes) - 6)
    top = max(0, min(b[1] for b in boxes) - 6)
    right = min(CELL, max(b[2] for b in boxes) + 6)
    bottom = min(CELL, max(b[3] for b in boxes) + 6)
    rows = list(preset()['states'])
    for group in range(2):
        tiles = []
        for state in rows[group * 7:(group + 1) * 7]:
            for frame in range(FRAMES):
                tile = work / f'{state}-{frame}-contact.png'
                bg = ('#ffffff', '#192635', '#ffcf58')[frame % 3]
                run_image([avatar_dir / catalog['states'][state]['atlas'], '-crop',
                           f'{right-left}x{bottom-top}+{frame*CELL+left}+{top}', '+repage',
                           '-background', bg, '-alpha', 'remove', '-alpha', 'off',
                           '-resize', '144x144', '-gravity', 'center', '-extent', '150x150', tile])
                tiles.append(tile)
        run_image([*tiles, '-tile', '10x7', '-geometry', '+2+2', '-background', '#64748b',
                   stage / f'contact-{group+1}.png'], mode='montage')


def package_avatar(folder, identifier, output, record=None):
    identifier = avatar_id(identifier)
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('Output exists; choose a new delivery directory.')
    report, catalog, blobs = inspect_avatar(folder)
    if not report['compatible']:
        raise ValueError('; '.join(report['errors']))
    creation = None
    if record:
        creation = read_json(record)
        if not isinstance(creation, dict) or set(creation) - {'tool', 'prompts', 'notes'}:
            raise ValueError('Creation record accepts only tool, prompts, and notes.')
    im_command(); im_command('montage')
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.avatar-delivery-', dir=output.parent))
    try:
        avatar_dir = stage / identifier
        avatar_dir.mkdir()
        write_json(avatar_dir / 'animations.json', catalog)
        for name, data in blobs.items():
            (avatar_dir / name).write_bytes(data)
        (stage / 'preview.html').write_text(render_preview(catalog, blobs), encoding='utf-8')
        write_json(stage / 'validation.json', report)
        instructions = (f'NEXIRUM — {catalog["name"]}\n\n'
                        f'Copy the {identifier} folder into resources/avatars/ beside NexirumCompanion.exe.\n'
                        'Select the mascot in Personal preferences → Appearance.\n'
                        'Keep other mascots intact. Configure the spoken wake name separately.\n\n'
                        'Open preview.html to try states, playback speed and backgrounds.\n'
                        'The preview works locally without network, microphone or AI.\n'
                        'Technical validation does not replace visual review or testing in the app.\n')
        (stage / 'INSTALL.txt').write_text(instructions, encoding='utf-8')
        if creation is not None:
            write_json(stage / 'creation.json', creation)
        with tempfile.TemporaryDirectory(prefix='avatar-contact-') as temporary:
            contact_sheets(catalog, report, avatar_dir, stage, Path(temporary))
        archive = stage / f'{identifier}.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for path in sorted(avatar_dir.iterdir()):
                z.write(path, f'{identifier}/{path.name}')
            for name in ('preview.html', 'validation.json', 'INSTALL.txt', 'creation.json'):
                path = stage / name
                if path.exists():
                    z.write(path, name)
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None:
                raise ValueError('Archive verification failed.')
            for name, data in blobs.items():
                if z.read(f'{identifier}/{name}') != data:
                    raise ValueError('Archive differs from validated atlas.')
        if output.exists():
            raise ValueError('Output appeared during processing; refusing replacement.')
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return {'output': str(output), 'archive': str(output / f'{identifier}.zip'),
            'preview': str(output / 'preview.html'), 'frames': 140,
            'warnings': report['warnings'], 'visual_review_required': True, 'app_runtime_tested': False}


def create_plan(args):
    avatar_id(args.id)
    if len(args.sheet) != len(args.rows):
        raise ValueError('Pair each --sheet with one --rows value.')
    states = []
    plan = {'avatar_id': args.id, 'name': args.name, 'reviewed': False, 'sheets': [], 'overrides': {}}
    for filename, row_names in zip(args.sheet, args.rows):
        source = Path(filename).resolve()
        rows = row_names.split(',')
        states += rows
        with Image.open(source) as im:
            width, height = im.size
        plan['sheets'].append({'source': str(source), 'states': rows,
                               'x_centers': [round((i + .5) * width / FRAMES, 2) for i in range(FRAMES)],
                               'y_edges': [round(i * height / len(rows)) for i in range(len(rows)+1)],
                               'scale': 1.0, 'alpha_levels': None})
    if len(states) != 14 or set(states) != set(preset()['states']):
        raise ValueError('Cover each of the 14 states exactly once.')
    path = Path(args.out).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(plan, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    return {'plan': str(path), 'reviewed': False, 'next': 'Inspect actual geometry before setting reviewed=true.'}


def pack_plan(filename, output, record=None):
    import numpy as np
    from scipy import ndimage

    path = Path(filename).resolve()
    plan = read_json(path)
    identifier = avatar_id(plan['avatar_id'])
    if plan.get('reviewed') is not True:
        raise ValueError('Inspect and adjust the proposed layout, then set reviewed=true.')
    config = preset()
    config['name'] = plan['name']
    states = [state for sheet in plan['sheets'] for state in sheet['states']]
    if len(states) != 14 or set(states) != set(config['states']):
        raise ValueError('Cover each preset state exactly once.')
    overrides = plan.get('overrides', {})
    allowed_keys = {f'{state}:{i}' for state in states for i in range(FRAMES)}
    if not isinstance(overrides, dict) or set(overrides) - allowed_keys:
        raise ValueError('Unexpected frame override.')
    with tempfile.TemporaryDirectory(prefix='avatar-pack-') as temporary:
        work = Path(temporary)
        avatar_dir = work / identifier
        avatar_dir.mkdir()
        for sheet_index, sheet in enumerate(plan['sheets']):
            source = (path.parent / sheet['source']).resolve()
            with Image.open(source) as original:
                original.load()
                if original.format not in ('PNG', 'WEBP') or getattr(original, 'is_animated', False) or 'A' not in original.getbands():
                    raise ValueError('Source must be a static PNG/WebP with actual alpha.')
                width, height = original.size
            copied = work / f'source-{sheet_index}{source.suffix}'
            copied.write_bytes(source.read_bytes())
            normalized = work / f'sheet-{sheet_index}.png'
            levels = sheet.get('alpha_levels')
            command = [copied]
            if levels is not None:
                if not isinstance(levels, list) or len(levels) != 2:
                    raise ValueError('alpha_levels must contain two normalized endpoints.')
                lo, hi = [number(v, 'alpha_levels') for v in levels]
                if not 0 <= lo < hi <= 1:
                    raise ValueError('Invalid alpha endpoints.')
                command += ['-channel', 'A', '-level', f'{lo*100}%,{hi*100}%', '+channel']
            run_image(command + [normalized])
            with Image.open(normalized) as image:
                alpha = np.array(image.getchannel('A'))
            if alpha.min() > 0 or alpha.max() < 240:
                raise ValueError('Source alpha is not suitable; inspect or repair the artwork.')
            centers = [number(v, 'x_centers') for v in sheet['x_centers']]
            edges = sheet['y_edges']
            if len(centers) != FRAMES or any(not 0 <= c < width for c in centers) or any(b <= a for a,b in zip(centers, centers[1:])):
                raise ValueError('x_centers must contain ten increasing in-bounds anchors.')
            if len(edges) != len(sheet['states'])+1 or any(type(v) is not int for v in edges) or edges[0] < 0 or edges[-1] > height or any(b <= a for a,b in zip(edges, edges[1:])):
                raise ValueError('Invalid y_edges.')
            scale = number(sheet.get('scale', 1), 'scale')
            if not 0 < scale <= 4:
                raise ValueError('Scale must be positive and at most four.')
            for row, state in enumerate(sheet['states']):
                y0, y1 = edges[row:row+2]
                cut_above = y0 > 0 and ((alpha[y0-1] > 192) & (alpha[y0] > 192)).sum() > 4
                cut_below = y1 < height and ((alpha[y1-1] > 192) & (alpha[y1] > 192)).sum() > 4
                if cut_above or cut_below:
                    raise ValueError(f'{state}: row boundary intersects artwork; adjust y_edges.')
                labels, count = ndimage.label(alpha[y0:y1] > 8, np.ones((3,3), dtype=int))
                objects = ndimage.find_objects(labels)
                areas = np.bincount(labels.ravel())
                groups = {i: [] for i in range(FRAMES)}
                for component, slices in enumerate(objects, 1):
                    if slices is None or areas[component] < 4:
                        continue
                    yy, xx = slices
                    owner = min(range(FRAMES), key=lambda i: abs(centers[i]-(xx.start+xx.stop-1)/2))
                    bx0, by0 = max(0, xx.start-1), max(y0, y0+yy.start-1)
                    bx1, by1 = min(width, xx.stop+1), min(y1, y0+yy.stop+1)
                    groups[owner].append([bx0, by0, bx1-bx0, by1-by0])
                frames = []
                for col in range(FRAMES):
                    override = overrides.get(f'{state}:{col}', {})
                    if not isinstance(override, dict) or set(override) - {'regions', 'anchor_x', 'baseline_y'}:
                        raise ValueError('Override accepts regions, anchor_x, and baseline_y only.')
                    center = number(override.get('anchor_x', centers[col]), 'anchor_x')
                    cx = round(center)
                    core = alpha[y0:y1, max(0,cx-32):min(width,cx+32)]
                    occupied = np.flatnonzero((core >= 192).sum(axis=1) > 3)
                    if not len(occupied) and 'baseline_y' not in override:
                        raise ValueError(f'{state}:{col}: missing body at anchor')
                    baseline = number(override['baseline_y'] if 'baseline_y' in override else y0+int(occupied[-1]), 'baseline_y')
                    regions = override.get('regions', groups[col])
                    if not isinstance(regions, list) or not regions:
                        raise ValueError(f'{state}:{col}: no regions')
                    command = ['-size', '256x256', 'xc:none']
                    for region in regions:
                        if not isinstance(region, list) or len(region) != 4 or any(type(v) is not int for v in region):
                            raise ValueError('Region must be four integers: x,y,width,height.')
                        x,y,w,h = region
                        if min(x,y) < 0 or min(w,h) <= 0 or x+w > width or y+h > height:
                            raise ValueError('Region is outside the source image.')
                        ox,oy = round(128+(x-center)*scale), round(239+(y-baseline)*scale)
                        sw,sh = max(1,round(w*scale)), max(1,round(h*scale))
                        if ox < 0 or oy < 0 or ox+sw > CELL or oy+sh > CELL:
                            raise ValueError(f'{state}:{col}: artwork would clip; inspect scale/anchors/regions')
                        command += ['(', normalized, '-crop', f'{w}x{h}+{x}+{y}', '+repage']
                        if scale != 1:
                            command += ['-resize', f'{sw}x{sh}!']
                        command += [')', '-geometry', f'+{ox}+{oy}', '-compose', 'Over', '-composite']
                    frame = work / f'{state}-{col}.png'
                    run_image(command + [frame])
                    frames.append(frame)
                run_image([*frames, '+append', '-define', 'webp:lossless=true', '-define',
                           'webp:method=6', '-define', 'webp:exact=true', '-quality', '100',
                           avatar_dir / config['states'][state]['atlas']])
        write_json(avatar_dir / 'animations.json', config)
        return package_avatar(avatar_dir, identifier, output, record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    check = sub.add_parser('check', help='Validate existing atlas files and the supplied preset.')
    check.add_argument('avatar')
    package = sub.add_parser('package', help='Validate and package an existing avatar.')
    package.add_argument('avatar'); package.add_argument('--id', required=True)
    package.add_argument('--out', required=True); package.add_argument('--record')
    plan = sub.add_parser('plan', help='Propose sheet geometry for visual inspection.')
    plan.add_argument('--id', required=True); plan.add_argument('--name', required=True)
    plan.add_argument('--sheet', action='append', required=True)
    plan.add_argument('--rows', action='append', required=True); plan.add_argument('--out', required=True)
    pack = sub.add_parser('pack', help='Pack reviewed geometry into a new complete avatar delivery.')
    pack.add_argument('plan'); pack.add_argument('--out', required=True); pack.add_argument('--record')
    args = parser.parse_args()
    try:
        if args.command == 'check':
            result, _, _ = inspect_avatar(args.avatar)
            status = 0 if result['compatible'] else 1
        elif args.command == 'plan':
            result, status = create_plan(args), 0
        elif args.command == 'package':
            result, status = package_avatar(args.avatar, args.id, args.out, args.record), 0
        else:
            result, status = pack_plan(args.plan, args.out, args.record), 0
    except (ValueError, OSError, TypeError, KeyError, ImportError, Image.DecompressionBombError) as exc:
        result, status = {'error': str(exc)}, 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return status


if __name__ == '__main__':
    sys.exit(main())
