"""Evaluate real held-out images via a running API; never generates fake results."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import urllib.request
import uuid


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--experiment',required=True)
    p.add_argument('--url',default='http://127.0.0.1:8000')
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--threshold',type=float,default=.7)
    args=p.parse_args()
    if not 0<=args.threshold<=1:p.error('threshold mesti antara 0 hingga 1')
    files=sorted(f for f in args.data.glob('*/*') if f.suffix.lower() in {'.jpg','.jpeg','.png','.webp'})
    if not files:sys.exit('Tiada imej ujian. Susun sebagai data/LABEL/imej.jpg.')
    rows=[]; matrix={}; seen=set()
    for file in files:
        data=file.read_bytes();digest=hashlib.sha256(data).hexdigest()
        if digest in seen:sys.exit('Imej pendua ditemui dalam set ujian: '+str(file))
        seen.add(digest)
        boundary=uuid.uuid4().hex
        body=(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="image"\r\n'
              f'Content-Type: application/octet-stream\r\n\r\n').encode()+data+f'\r\n--{boundary}--\r\n'.encode()
        request=urllib.request.Request(args.url+'/predict?threshold='+str(args.threshold),data=body,
                    headers={'Content-Type':'multipart/form-data; boundary='+boundary})
        with urllib.request.urlopen(request,timeout=60) as response:pred=json.load(response)
        actual=file.parent.name
        rows.append(dict(experiment=args.experiment,file=str(file),sha256=digest,actual=actual,
                         top_class=pred['top_class'],prediction=pred['prediction'],
                         confidence=pred['confidence'],threshold=args.threshold,
                         correct=actual==pred['top_class'],accepted_correct=actual==pred['prediction']))
        matrix.setdefault(actual,{})
        matrix[actual][pred['top_class']]=matrix[actual].get(pred['top_class'],0)+1
    args.out.mkdir(parents=True,exist_ok=True)
    path=args.out/(args.experiment+'.csv')
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    n=len(rows);accepted=[r for r in rows if r['prediction']!='UNKNOWN']
    summary=dict(experiment=args.experiment,total=n,top1_accuracy=sum(r['correct'] for r in rows)/n,
                 accepted_correct_over_all=sum(r['accepted_correct'] for r in rows)/n,
                 coverage=len(accepted)/n,
                 accuracy_among_accepted=sum(r['accepted_correct'] for r in accepted)/len(accepted) if accepted else None,
                 threshold=args.threshold,confusion_matrix_top1=matrix)
    (args.out/(args.experiment+'.json')).write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
