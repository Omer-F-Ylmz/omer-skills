import re,sys,json
from pathlib import Path
sys.path.insert(0,'tools'); sys.argv=['x']
import importlib.util
src=Path('tools/video_derin.py').read_text(encoding='utf-8')
m=re.search(r"def kod_of.*?\n(?=\ndef |\n\S)",src,re.S); ns={'re':re}; exec("import re\n"+m.group(0),ns); kod_of=ns['kod_of']
t=Path('.kos/kopru/linkler-2026-10-23-telefon.txt').read_text(encoding='utf-8')
o=Path('.kos/kopru/linkler-2026-10-23-omer.tsv').read_text(encoding='utf-8').splitlines()[1:]
sil={l.strip() for l in Path('.kos/kopru/ig-silinen.txt').read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')}
urls=list(dict.fromkeys(re.findall(r'https?://\S+',t)+[l.split('\t')[1] for l in o if '\t' in l and 'github.com' not in l]))
tum={};
for u in urls: tum.setdefault(kod_of(u),u)
yap=[k for k in tum if Path(f'docs/video-tarama/derin/{k}.json').exists()]
sl=[k for k in tum if k in sil]
bek=[k for k in tum if k not in yap and k not in sil]
print(len(urls),len(tum),'yapilmis',len(yap),'silinmis',len(sl),'bekleyen',len(bek))
Path('.kos/kopru/ara/dy1_bekleyen.txt').write_text('\n'.join(tum[k] for k in bek),encoding='utf-8')
json.dump({'tum':tum,'sil':sl},open('.kos/kopru/ara/dy1_tum.json','w'))
