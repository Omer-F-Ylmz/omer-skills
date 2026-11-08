"""F9: oturumlar arası mesaj kuyruğu (dosya tabanlı, ağ yok). gonder: oturum_mesaj.py gonder <alici> "<metin>" [--kimden X]; al: oturum_mesaj.py al <alici> (okunmamışları basar, okundu işaretler).
Kuyruk: .kos/kopru/mesaj/<alici>.jsonl (gitignore'lu .kos altında). Hermes ayrı: ajan_sira motor=hermes iş olarak bu kuyruğu `al` ile okuyabilir (bağlanmadı).
Kendini sınama: oturum_mesaj.py test"""
import json, sys, tempfile, time
from pathlib import Path
DIZIN = Path(r"C:\Projeler\omer-skills\.kos\kopru\mesaj")

def gonder(alici, metin, kimden="?", dizin=DIZIN):
    dizin.mkdir(parents=True, exist_ok=True)
    with open(dizin / f"{alici}.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "kimden": kimden, "metin": metin, "okundu": False}, ensure_ascii=False) + "\n")

def al(alici, dizin=DIZIN):
    p = dizin / f"{alici}.jsonl"
    if not p.exists(): return []
    kayit = [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
    yeni = [k for k in kayit if not k["okundu"]]
    for k in kayit: k["okundu"] = True
    p.write_text("".join(json.dumps(k, ensure_ascii=False) + "\n" for k in kayit), encoding="utf-8")
    return yeni

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["test"]:
        d = Path(tempfile.mkdtemp())
        gonder("x", "merhaba", "t", d); gonder("x", "ikinci", "t", d)
        assert [m["metin"] for m in al("x", d)] == ["merhaba", "ikinci"] and al("x", d) == [] and al("yok", d) == []
        print("OK 3/3")
    elif a[:1] == ["gonder"]:
        gonder(a[1], a[2], a[a.index("--kimden") + 1] if "--kimden" in a else "?")
    elif a[:1] == ["al"]:
        for m in al(a[1]): print(f"[{m['t']}] {m['kimden']}: {m['metin']}")
