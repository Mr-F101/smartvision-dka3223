"""Record live HTTP integration checks using the selected, real model."""
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
import httpx

def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser()
    parser.add_argument('--url',default='http://127.0.0.1:8000')
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():
        parser.error('Fail bukti sudah wujud. Pilih nama baharu.')
    client=httpx.Client(base_url=args.url,timeout=30,trust_env=False)
    health=client.get('/health').json()
    assert health['model_ready'] and health['labels']==['BOTOL','BUKU','TELEFON']
    image=next((root/'dataset_public'/'test'/'BOTOL').glob('*.jpg')).read_bytes()
    cases=[('API01',image,.7,200),('API02',b'',.7,400),
           ('API03',b'x'*(8*1024*1024+1),.7,413),('API04',image,1.1,422),
           ('API05',b'not an image',.7,400)]
    results=[]
    for name,data,threshold,expected in cases:
        response=client.post('/predict',params={'threshold':threshold},files={'file':('image.jpg',data,'image/jpeg')})
        results.append({'id':name,'expected_status':expected,'actual_status':response.status_code,
                        'passed':response.status_code==expected,'response':response.json()})
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'method':'Live HTTP integration checks, not manual browser tests',
            'health':health,'checks':results}
    out=args.out
    if out.exists():
        raise RuntimeError('Refusing to overwrite previous evidence')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    client.close()
    print(json.dumps(report,indent=2))
    assert all(r['passed'] for r in results)

if __name__=='__main__':
    main()
