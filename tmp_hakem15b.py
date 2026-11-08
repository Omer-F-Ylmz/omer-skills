import sys, json, glob, os
sys.path.insert(0, "tools")
import usta_kart as u
d = ".kos/kopru/usta-haiku/ileri/"
man = json.load(open(d + "manifest.json", encoding="utf-8"))
ad = json.load(open(d + "hakem15-adlar.json", encoding="utf-8"))
C = {json.loads(l)["ad"]: json.loads(l) for l in open(d + "tur15.jsonl", encoding="utf-8") if l.strip()}
for g in range(4):
    par = []
    for j, a in enumerate(ad[g*10:(g+1)*10]):
        i = man.index(a)
        fl = sorted(glob.glob(os.path.abspath(d + f"kaynak/{i}_*.txt")))
        par.append(f"[{j}] {a} | kaynak parça dosyaları (HEPSİNİ Read ile oku): {' ; '.join(fl)}\n kart: {json.dumps({x: C[a][x] for x in u.ALANLAR}, ensure_ascii=False)}")
    ist = ("Hakemsin. Her kart için kaynak parçalarının TAMAMINI okuyup karar ver: DOĞRU (kartta kaynakta olmayan/çelişen iddia yok) ve YARARLI (somut, genel geçer değil) mi? "
           "Kaynakta gerçekten aradığın şeyi bulamadan 'yok' deme. YALNIZ JSON dizisi: [{\"i\":0,\"dogru\":true,\"yararli\":true,\"neden\":\"≤10 kelime\"}...]\n\n" + "\n".join(par))
    open(d + f"hakem15b-{g}.txt", "w", encoding="utf-8").write(ist)
print("ok")
