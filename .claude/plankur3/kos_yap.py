"""PLAN-KUR-2 kos.py → PLAN-KUR-3 kos.py (yerine koyma; her biri tam 1 kez eşleşmeli)."""
from pathlib import Path

D = Path(__file__).resolve().parent
s = (D.parent / "plankur2" / "kos.py").read_text(encoding="utf8")
R = [
    ('"""PLAN-KUR-2 ölçüm: bekletilmiş 10 iş (tests/fixtures/plan_kur2_isler.tsv)', '"""PLAN-KUR-3 ölçüm: YENİ bekletilmiş 10 iş (tests/fixtures/plan_kur3_isler.tsv, 913dcc7)'),
    ('A = main katalog_ara (ba051cb), B = plan_kur v2.', 'A = main katalog_ara (e05750a), B = plan_kur v3.'),
    ('import plan_kur as pk  # noqa: E402\n', 'import plan_kur as pk  # noqa: E402\nimport katalog_ara as ka  # noqa: E402\n'),
    ('katalog_ara.py")  # main ba051cb', 'katalog_ara.py")  # main e05750a'),
    ('"plan_kur2_isler.tsv"', '"plan_kur3_isler.tsv"'),
    ('listeyi oku, ek sorgu yapma. Rutin', 'listeyi oku, ek sorgu yapma (çıktı dosyaya düşerse yalnız o iş için --aday 40 ile yeniden). Rutin'),
    ('yasak = pk.kurulu_disi_adlar()\n',
     '# görev madde 4: yalnız katalogdaki TAM araç adları (kurulu olmayan, kurulu bir adla aynı olmayan); tek sözcüklü ≤4 harf ad gürültü\n'
     'kur = {o["ad"].lower() for o in pk.kayitlar() if ka.kurulu(o)}\n'
     'yasak = {o["ad"].lower() for o in pk.kayitlar() if not ka.kurulu(o) and (len(o["ad"]) > 4 or "-" in o["ad"] or ":" in o["ad"])} - kur\n'),
    (r're.search(rf"\b{re.escape(w)}\b", parca[k].lower())', r're.search(rf"(?<![\w:-]){re.escape(w)}(?![\w-])", parca[k].lower())'),
    ('f"rutin jeton A', 'f"paket jeton A/B {[(top(\'A\', [p]), top(\'B\', [p])) for p in range(4)]}\\n"\n        f"rutin jeton A'),
]
for a, b in R:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
(D / "kos.py").write_bytes(s.encode("utf8"))
