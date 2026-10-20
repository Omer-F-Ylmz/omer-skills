"""RUFLO-2 d2 C: karma 0.0 kök neden. Kuyruk kayıtlarını (.islendi/.jsonl 'bitti') ayrıştırır: ajan × (son boş · test · hata · araç) × karma.
python sifir_kok.py → özet satırlar (salt okuma, ücretsiz)"""
import collections, json, sys
from pathlib import Path

K = Path("C:/Projeler/omer-skills/.kos/ogrenme/kuyruk")
# karma kuyrukta saklanmaz: kanca.log "oturum8 ... karma [..]" satırını oturumun son-5 'bitti' kaydıyla eşle
import re
ks = []
for ln in (K.parent / "kanca.log").read_text(encoding="utf-8").splitlines():
    m = re.search(r"\d\d:\d\d:\d\d (\w{8}) yargı \d+ · karma \[([^\]]*)\]", ln)
    f = m and next(K.glob(m[1] + "*"), None)
    if not f:
        continue
    bitti = [x for x in map(json.loads, f.read_text(encoding="utf-8", errors="replace").splitlines() if True else []) if x.get("tip") == "bitti"][-5:]
    for x, k in zip(bitti, m[2].split(",")):
        if k.strip() != "None":
            ks.append({**x, "karma": float(k)})
kay = ks
sys.stdout.reconfigure(encoding="utf-8")
print("bitti kayıt", len(kay), "alanlar", sorted(kay[0]) if kay else "-")
print("karma yazılı", len(ks))
sf = [x for x in ks if x["karma"] == 0]
print(f"karma=0: {len(sf)}/{len(ks)}")


def say(ad, f):
    a = [x for x in ks if f(x)]
    print(f"  {ad}: n={len(a)} sıfır=%{100 * sum(x['karma'] == 0 for x in a) / max(len(a), 1):.0f}")


say("son boş", lambda x: not (x.get("son") or "").strip())
say("son dolu", lambda x: (x.get("son") or "").strip())
say("test=None", lambda x: x.get("test") is None)
say("test=1", lambda x: x.get("test") == 1)
say("test=0", lambda x: x.get("test") == 0)
say("hata=0", lambda x: x["hata"] == 0)
say("hata>0", lambda x: x["hata"] > 0)
say("baglam yok (kural belgesi/teslim)", lambda x: not x.get("baglam"))
say("baglam var", lambda x: x.get("baglam"))
say("arac<5", lambda x: x["arac"] < 5)
say("arac>=5", lambda x: x["arac"] >= 5)
for a, n in collections.Counter(x["ajan"] for x in ks).most_common(5):
    say(f"ajan {a}", lambda x, a=a: x["ajan"] == a)
