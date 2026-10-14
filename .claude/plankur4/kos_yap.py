"""PLAN-KUR-4 koşucusu: .claude/plankur3d4/kos.py'den üç kollu (A main katalog_ara · B plan_kur v4 · C = B' v3 kurulu skill) kos.py üretir."""
from pathlib import Path

D = Path(__file__).resolve().parent
s = (D.parent / "plankur3d4" / "kos.py").read_text(encoding="utf8")
DEG = [
    ("PLAN-KUR-3 ölçüm: YENİ bekletilmiş 10 iş (tests/fixtures/plan_kur3_isler.tsv, 913dcc7), 4 paket × A/B = 8 claude -p + kör yargıç 1 = 9 (tavan 10).\n"
     "A = main katalog_ara (e05750a), B = plan_kur v3.",
     "PLAN-KUR-4 ölçüm: YENİ bekletilmiş 10 iş (tests/fixtures/plan_kur4_isler.tsv, 02e1820), 4 paket × A/B/C = 12 claude -p + kör yargıç 1 = 13 (tavan 13).\n"
     "A = main katalog_ara (bugünkü), B = plan_kur v4, C = B' plan_kur v3 (kurulu skill ~/.claude/skills/plan-kur, 8b3b11c ile aynı)."),
    ("# main e05750a", "# main bugünkü"),
    ("plan_kur3_isler.tsv", "plan_kur4_isler.tsv"),
    ("PLAN_KUR = WT / \"tools\" / \"plan_kur.py\"\n",
     "PLAN_KUR = WT / \"tools\" / \"plan_kur.py\"\nV3 = Path.home() / \".claude\" / \"skills\" / \"plan-kur\" / \"plan_kur.py\"\n"),
    ("         f\"ek sorgu yapma. Rutin işte çağırma.\\n\\n\",\n}\n",
     "         f\"ek sorgu yapma. Rutin işte çağırma.\\n\\n\",\n}\nKURAL[\"C\"] = KURAL[\"B\"].replace(str(PLAN_KUR), str(V3))\n"),
    ("iki plan var (X ve Y; kaynakları gizli)", "üç plan var (X, Y ve Z; kaynakları gizli)"),
    ("\\\"Y\\\": [k,s,a,u]}, ...}", "\\\"Y\\\": [k,s,a,u], \\\"Z\\\": [k,s,a,u]}, ...}"),
    ("for kol in (\"A\", \"B\"):", "for kol in (\"A\", \"B\", \"C\"):"),
    ("kd = {\"A\": set(), \"B\": set()}", "kd = {\"A\": set(), \"B\": set(), \"C\": set()}"),
    ("    for k in \"AB\":", "    for k in \"ABC\":"),
    ("for k in \"AB\"}", "for k in \"ABC\"}"),
    ("        x = random.choice(\"AB\")\n"
     "        anahtar[n + 1] = {\"X\": x, \"Y\": \"B\" if x == \"A\" else \"A\"}\n"
     "        kor.append(f\"## {n + 1}. {IS[n]}\\n### X\\n{parca[x][:5000]}\\n### Y\\n{parca[anahtar[n + 1][\"Y\"]][:5000]}\\n\")\n",
     "        sira = random.sample(\"ABC\", 3)\n"
     "        anahtar[n + 1] = dict(zip(\"XYZ\", sira))\n"
     "        kor.append(f\"## {n + 1}. {IS[n]}\\n\" + \"\".join(f\"### {xy}\\n{parca[k][:5000]}\\n\" for xy, k in zip(\"XYZ\", sira)))\n"),
    ("puan = {\"A\": 0, \"B\": 0}", "puan = {\"A\": 0, \"B\": 0, \"C\": 0}"),
    ("for xy in \"XY\":", "for xy in \"XYZ\":"),
    ("{sorted(kd['B'])}\")\n",
     "{sorted(kd['B'])}\\n\"\n"
     "        f\"C=B' v3: kalite {puan['C']} · zor jeton {top('C', [0, 1, 2])} · tur {tur('C', [0, 1, 2])} · rutin jeton {top('C', [3])} · \"\n"
     "        f\"paket jeton {[top('C', [p]) for p in range(4)]} · kurulu-olmayan {len(kd['C'])} {sorted(kd['C'])}\")\n"),
]
for eski, yeni in DEG:
    assert s.count(eski) == 1, eski[:60]
    s = s.replace(eski, yeni)
(D / "kos.py").write_text(s, encoding="utf8")
