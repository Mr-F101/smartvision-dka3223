"""Build an attributed Open Images subset; preserve the user's original dataset.

Run from SmartClassifier. Uses cached official annotation CSVs in ../.build/openimages.
Original image bytes are preserved; no augmentation or synthetic samples are created.
"""
import csv
import hashlib
import json
import random
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT.parent / '.build' / 'openimages'
OUT = ROOT / 'dataset_public'
EVIDENCE = ROOT / 'evidence' / 'public_dataset'
LABELS = {'/m/0bt_c3': 'BUKU', '/m/04dr76w': 'BOTOL', '/m/050k8': 'TELEFON'}


def main():
    candidates = {}
    for file in ('boxes.csv', 'test-boxes.csv'):
        with (CACHE / file).open(encoding='utf-8') as stream:
            for row in csv.DictReader(stream):
                if row['LabelName'] not in LABELS:
                    continue
                if any(row[k] != '0' for k in ('IsGroupOf', 'IsDepiction', 'IsOccluded', 'IsTruncated')):
                    continue
                area = (float(row['XMax'])-float(row['XMin']))*(float(row['YMax'])-float(row['YMin']))
                if area < .05:
                    continue
                key = row['ImageID']
                if key not in candidates or candidates[key]['area'] < area:
                    candidates[key] = {'label': LABELS[row['LabelName']], 'area': area}
    for file in ('images.csv', 'test-images.csv'):
        with (CACHE / file).open(encoding='utf-8') as stream:
            for row in csv.DictReader(stream):
                if row['ImageID'] in candidates:
                    candidates[row['ImageID']].update(row)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    originals = CACHE / 'originals'
    originals.mkdir(exist_ok=True)
    selected = []
    authors = set()
    # Books first because they have the fewest eligible images.
    for label in ('BUKU', 'BOTOL', 'TELEFON'):
        count = 0
        for row in sorted(candidates.values(), key=lambda r: (-r['area'], r.get('ImageID', ''))):
            if row['label'] != label or row.get('License') != 'https://creativecommons.org/licenses/by/2.0/':
                continue
            author = row.get('AuthorProfileURL')
            if not author or author in authors:
                continue
            authors.add(author)
            selected.append(row)
            count += 1
            if count == 80:
                break
        if count < 70:
            raise RuntimeError(f'Insufficient independent sources for {label}: {count}')

    def download(row):
        file = originals / (row['ImageID'] + '.jpg')
        url = f"https://open-images-dataset.s3.amazonaws.com/{row['Subset']}/{row['ImageID']}.jpg"
        try:
            if not file.exists():
                with urllib.request.urlopen(url, timeout=45) as response:
                    data = response.read()
                file.write_bytes(data)
            with Image.open(file) as image:
                image.verify()
            row['download_url'] = url
            row['sha256'] = hashlib.sha256(file.read_bytes()).hexdigest()
            return row
        except Exception as exc:
            print(f"FAILED {row['ImageID']}: {exc}", flush=True)
            return None

    with ThreadPoolExecutor(max_workers=6) as executor:
        downloaded = [r for r in executor.map(download, selected) if r]
    (EVIDENCE / 'candidates.json').write_text(json.dumps(downloaded, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Downloaded candidates:', {label: sum(r['label']==label for r in downloaded) for label in LABELS.values()}, flush=True)
    # Contact sheets are QA previews; training images remain unchanged.
    for label in LABELS.values():
        rows = [r for r in downloaded if r['label']==label]
        for page in range(0, len(rows), 20):
            sheet = Image.new('RGB', (1000, 1000), 'white')
            draw = ImageDraw.Draw(sheet)
            for i, row in enumerate(rows[page:page+20]):
                with Image.open(originals / (row['ImageID']+'.jpg')) as im:
                    thumb = ImageOps.contain(ImageOps.exif_transpose(im).convert('RGB'), (195, 215))
                    x, y = (i%5)*200, (i//5)*250
                    sheet.paste(thumb, (x, y))
                    draw.text((x+2,y+217), f"{page+i}: {row['ImageID']}", fill='black')
            sheet.save(EVIDENCE / f'qa_{label}_{page//20+1}.jpg')


if __name__ == '__main__':
    main()
