import json,sys
ids="DcG5MjqOVYp DcBuc3XuVif DbEK3bustQ7 DZ0BCZYO27X DYUmHtwutIl DeMz56LkwOL DYCll4ROMoa".split()
for k in ids:
    d=json.load(open(f'docs/video-tarama/derin/{k}.json',encoding='utf-8'))
    m=d['meta']; seen=[];s=set()
    for e in d['ekran']:
        t=e['t'].strip()
        if len(t)>=5 and t not in s: s.add(t);seen.append(t)
    o=[f"# {k} (link-30eki, ARA KAYIT, otomatik derin tarama; OCR gurultulu)",
       f"Yukleyen: {m.get('yukleyen')} | sure: {m.get('sure')}s | ASR: {d.get('asr')} | kare: {d.get('kare_sayisi')}",
       "\n## Caption\n"+(m.get('aciklama') or ''),
       "\n## Konusma\n"+"\n".join(f"- [{x['b']}-{x['s']}s] {x['t']}" for x in d['transkript']),
       "\n## Ekranda gorunen (OCR, tekrarsiz)\n"+"\n".join("- "+t for t in seen[:120]),
       "\n## Linkler (OCR)\n"+"\n".join("- "+x for x in d['linkler']),
       "\n## Komutlar\n"+"\n".join("- "+x.replace("\n"," / ") for x in d['komutlar']),
       "\n## Kare aciklamalari\n"+json.dumps(d.get('kare_aciklama'),ensure_ascii=False)[:1500]]
    open(f'.kos/kopru/video/link-30eki/{k}.md','w',encoding='utf-8').write("\n".join(o))
    print(k,len(seen))
