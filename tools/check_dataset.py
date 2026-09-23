"""Check exact duplicates, labels and image counts before training/testing."""
from pathlib import Path
import hashlib
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'dataset')
seen={}; failures=[]
for split in ['train_e1','train_e2','validation','test']:
    for label in ['BOTOL','BUKU','TELEFON']:
        directory=root/split/label
        files=[f for f in directory.glob('*') if f.suffix.lower() in {'.jpg','.jpeg','.png','.webp'}]
        print(f'{split}/{label}: {len(files)}')
        if not files:failures.append('Folder kosong: '+str(directory))
        local=set()
        for f in files:
            digest=hashlib.sha256(f.read_bytes()).hexdigest()
            if digest in local:failures.append('Pendua dalam folder: '+str(f))
            local.add(digest)
            for prior_split,prior_label,prior in seen.get(digest,[]):
                if prior_label!=label or ({split,prior_split}!={'train_e1','train_e2'}):
                    failures.append('Pertindihan / label bercanggah: '+str(prior)+' dan '+str(f))
            seen.setdefault(digest,[]).append((split,label,f))
print('\n'.join(failures) if failures else 'Tiada pendua tepat merentasi split. Semak juga imej hampir sama secara manual.')
sys.exit(1 if failures else 0)
