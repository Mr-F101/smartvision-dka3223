"""Freeze manually reviewed public images into independent project splits."""
import csv
import hashlib
import json
import random
import shutil
import zipfile
from prepare_public_dataset import CACHE, EVIDENCE, OUT

BOOKS = [0,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,24,26,27,28,31,32,34,36,38,40,43,44,45,46,50,55,56,65,69]
EXTRA_BOOKS = [0,1,2,3,4,6,7,8,9,10,12,14,15,16,17,18,19,20,21,22,23,25,27,28,32,34,35,36,38,40]
BOTTLE_REJECT = {1, 9, 17, 19, 29, 33, 56, 58, 60, 77}
PHONE_REJECT = {3, 4, 12, 24, 37, 40, 44, 56, 2, 50}

def main():
    original = json.loads((EVIDENCE/'candidates.json').read_text(encoding='utf-8'))
    extra = json.loads((EVIDENCE/'extra_books.json').read_text(encoding='utf-8'))
    groups = {label:[r for r in original if r['label']==label] for label in ('BOTOL','BUKU','TELEFON')}
    chosen = {
        'BUKU':[groups['BUKU'][i] for i in BOOKS]+[extra[i] for i in EXTRA_BOOKS],
        'BOTOL':[r for i,r in enumerate(groups['BOTOL']) if i not in BOTTLE_REJECT],
        'TELEFON':[r for i,r in enumerate(groups['TELEFON']) if i not in PHONE_REJECT],
    }
    manifest=[]
    assert all(len(rows)==70 for rows in chosen.values())
    allrows=[r for rows in chosen.values() for r in rows]
    assert len({r['ImageID'] for r in allrows})==210
    assert len({r['sha256'] for r in allrows})==210
    assert len({r['AuthorProfileURL'] for r in allrows})==210
    OUT.mkdir(exist_ok=True)
    for label,rows in chosen.items():
        random.Random('SmartVision-20260924-'+label).shuffle(rows)
        for i,r in enumerate(rows):
            split='train_e1' if i<50 else 'validation' if i<60 else 'test'
            for targetsplit in ([split,'train_e2'] if split=='train_e1' else [split]):
                target=OUT/targetsplit/label/(r['ImageID']+'.jpg')
                target.parent.mkdir(parents=True,exist_ok=True)
                source=CACHE/'originals'/(r['ImageID']+'.jpg')
                if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=r['sha256']:
                    raise RuntimeError('Refusing to overwrite changed image: '+str(target))
                shutil.copy2(source,target)
            manifest.append(dict(r,project_split=split,review='visual_contact_sheet_accepted',modification='none'))
    (EVIDENCE/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    fields=['ImageID','label','project_split','Subset','Author','Title','AuthorProfileURL','OriginalLandingURL','License','download_url','sha256','modification']
    with (EVIDENCE/'attribution.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(manifest)
    for label in chosen:
        with zipfile.ZipFile(OUT/(label+'_train.zip'),'w',zipfile.ZIP_DEFLATED) as z:
            for file in sorted((OUT/'train_e1'/label).glob('*.jpg')):
                z.write(file,file.name)
    print('Frozen: 210 unique originals; 50 train + 10 validation + 10 test per class.')
    print('E1/E2 share training intentionally; no image hash or source author shared with holdout.')

if __name__=='__main__':
    main()
