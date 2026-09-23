"""Compare outputs of evaluate.py only when the evaluation protocol matches."""
import argparse
import json
from pathlib import Path


def compare(first, second):
    for result in (first, second):
        if not result.get('model_id') or not result.get('dataset'):
            raise ValueError('Keputusan mesti dijana oleh evaluate.py terkini dengan cap jari model dan dataset.')
        if result['total'] != len(result['dataset']):
            raise ValueError('Jumlah imej tidak sepadan dengan manifest dataset.')
        if len({r['sha256'] for r in result['dataset']}) != result['total']:
            raise ValueError('Dataset mengandungi imej pendua.')
    key=lambda data: sorted((r['sha256'],r['actual']) for r in data['dataset'])
    if key(first)!=key(second):
        raise ValueError('E1 dan E2 mesti diuji pada imej serta label sebenar yang sama.')
    if first['threshold']!=second['threshold']:
        raise ValueError('Threshold E1 dan E2 berbeza.')
    if first['model_id']==second['model_id']:
        raise ValueError('Kedua-dua keputusan menggunakan fail model dan label yang sama. Semak eksport E1/E2.')
    metrics=['top1_accuracy','coverage','accuracy_among_accepted','accepted_correct_over_all']
    for result in (first,second):
        for field in metrics:
            value=result[field]
            if value is None and field=='accuracy_among_accepted':continue
            if not isinstance(value,(int,float)) or not 0<=value<=1:raise ValueError('Metrik tidak sah: '+field)
    pct=lambda value:'Tidak ditakrifkan' if value is None else f'{value*100:.2f}%'
    names={'top1_accuracy':'Accuracy top 1','coverage':'Coverage',
           'accuracy_among_accepted':'Accuracy dalam ramalan diterima',
           'accepted_correct_over_all':'Ramalan diterima betul / semua imej'}
    lines=['# Perbandingan eksperimen sebenar','',
           f"Jumlah imej sama: {first['total']}. Threshold: {first['threshold']:.2f}.",'',
           '| Ukuran | '+first['experiment']+' | '+second['experiment']+' |',
           '|---|---:|---:|']
    lines += [f'| {names[m]} | {pct(first[m])} | {pct(second[m])} |' for m in metrics]
    lines += ['', 'Gunakan keputusan validation untuk pemilihan model. Nilai test akhir selepas model dipilih.',
              'Semak confusion matrix dan kesilapan setiap kelas sebelum membuat kesimpulan.', '',
              'Model pertama: '+first['model_id'], 'Model kedua: '+second['model_id']]
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('first',type=Path);parser.add_argument('second',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        output=compare(json.loads(args.first.read_text()),json.loads(args.second.read_text()))
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('x',encoding='utf-8') as f:f.write(output)
    except (ValueError,KeyError,OSError) as exc:parser.exit(1,str(exc)+'\n')
    print(args.out)
