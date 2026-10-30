# usta.jsonl'de geçersiz JSON kaçışı (C:\AI gibi tek ters eğik) olan satırları onarır; içerik değişmez
import json, re
p = r"C:\Projeler\omer-skills\docs\usta-kart\usta.jsonl"
L = open(p, "rb").read().decode("utf-8").split("\n")
n = 0
for i, l in enumerate(L):
    if not l.strip():
        continue
    try:
        json.loads(l)
    except json.JSONDecodeError:
        f = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", l)
        json.loads(f)
        L[i], n = f, n + 1
open(p, "wb").write("\n".join(L).encode("utf-8"))
print("onarildi", n)
