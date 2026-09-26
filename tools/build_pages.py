"""Build the public browser-only app; never publish datasets or Python files."""
import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build(out):
    out = Path(out).resolve()
    if out == ROOT or out in ROOT.parents:
        raise ValueError('Output must be a separate build directory.')
    out.mkdir(parents=True, exist_ok=True)
    html = (ROOT / 'static/index.html').read_text(encoding='utf-8')
    replacements = {
        '<html lang="ms">': '<html lang="ms" data-deployment="pages">',
        'href="/docs"': 'href="https://github.com/Mr-F101/smartvision-dka3223"',
        'Dokumentasi API ↗': 'Tentang projek ↗',
        '<label for="mode">Kaedah inferens</label><select id="mode"><option value="browser">Pelayar · TensorFlow.js</option><option value="api">Python · FastAPI</option></select>': '<input id="mode" type="hidden" value="browser"><p>Model E2 · Botol, buku dan telefon. Imej diproses pada peranti anda.</p>',
        '<div id="url-field">': '<div id="url-field" hidden>',
        '<option>E1</option><option selected>E2</option>': '<option selected>E2</option>',
        'Gunakan model terlatih untuk memulakan ramalan.': 'Model dimuatkan secara automatik. Kemudian pilih imej atau buka kamera.',
    }
    for old, new in replacements.items():
        if html.count(old) != 1:
            raise ValueError(f'Expected one template marker: {old}')
        html = html.replace(old, new)
    (out / 'index.html').write_text(html, encoding='utf-8')
    (out / '.nojekyll').touch()
    (out / 'static').mkdir(exist_ok=True)
    for name in ('style.css', 'script.js'):
        shutil.copy2(ROOT / 'static' / name, out / 'static' / name)
    shutil.copytree(ROOT / 'static/vendor', out / 'static/vendor', dirs_exist_ok=True)
    model = ROOT / 'models/tfjs'
    manifest = json.loads((model / 'model.json').read_text())
    names = ['model.json', 'metadata.json']
    names += [name for group in manifest['weightsManifest'] for name in group['paths']]
    target = out / 'models/tfjs'
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        source = (model / name).resolve()
        if source.parent != model.resolve():
            raise ValueError('Model weights must reside directly in the export folder.')
        shutil.copy2(source, target / name)
    assert 'value="api"' not in html and 'href="/docs"' not in html
    assert 'value="./models/tfjs/"' in html
    print(f'Public app built: {out}; {len(names)} model files, browser inference only.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / '_site')
    build(parser.parse_args().out)
