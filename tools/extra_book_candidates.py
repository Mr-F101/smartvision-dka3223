"""Retrieve additional annotated book photographs for manual review, not final data."""
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps, ImageDraw
from prepare_public_dataset import CACHE, EVIDENCE
import urllib.request
import hashlib

def main():
    prior = json.loads((EVIDENCE / 'candidates.json').read_text(encoding='utf-8'))
    ids = {r['ImageID'] for r in prior}
    authors = {r['AuthorProfileURL'] for r in prior}
    found = {}
    for filename in ('boxes.csv', 'test-boxes.csv'):
        with (CACHE / filename).open(encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r['LabelName'] != '/m/0bt_c3' or r['ImageID'] in ids:
                    continue
                if r['IsGroupOf'] != '0' or r['IsDepiction'] != '0':
                    continue
                area = (float(r['XMax'])-float(r['XMin']))*(float(r['YMax'])-float(r['YMin']))
                if area < .10:
                    continue
                if r['ImageID'] not in found or area > found[r['ImageID']]['area']:
                    found[r['ImageID']] = dict(r, area=area, label='BUKU')
    for filename in ('images.csv', 'test-images.csv'):
        with (CACHE / filename).open(encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r['ImageID'] in found:
                    found[r['ImageID']].update(r)
    chosen = []
    for r in sorted(found.values(), key=lambda r: -r['area']):
        if r.get('License') != 'https://creativecommons.org/licenses/by/2.0/' or not r.get('AuthorProfileURL') or r['AuthorProfileURL'] in authors:
            continue
        authors.add(r['AuthorProfileURL'])
        chosen.append(r)
        if len(chosen) == 100:
            break
    def download(r):
        dest = CACHE / 'originals' / (r['ImageID']+'.jpg')
        url = f"https://open-images-dataset.s3.amazonaws.com/{r['Subset']}/{r['ImageID']}.jpg"
        try:
            if not dest.exists():
                with urllib.request.urlopen(url, timeout=45) as response:
                    dest.write_bytes(response.read())
            with Image.open(dest) as im:
                im.verify()
            r.update(download_url=url, sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
            return r
        except Exception as exc:
            print(r['ImageID'], str(exc), flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = [r for r in pool.map(download, chosen) if r]
    (EVIDENCE/'extra_books.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Extra books for manual review:', len(rows), flush=True)
    for page in range(0,len(rows),20):
        sheet=Image.new('RGB',(1000,1000),'white')
        draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(rows[page:page+20]):
            with Image.open(CACHE/'originals'/(r['ImageID']+'.jpg')) as im:
                thumb=ImageOps.contain(ImageOps.exif_transpose(im).convert('RGB'),(195,215))
                x,y=(i%5)*200,(i//5)*250
                sheet.paste(thumb,(x,y))
                draw.text((x+2,y+217),f"{page+i}: {r['ImageID']}",fill='black')
        sheet.save(EVIDENCE/f'qa_EXTRA_BUKU_{page//20+1}.jpg')

if __name__ == '__main__':
    main()
