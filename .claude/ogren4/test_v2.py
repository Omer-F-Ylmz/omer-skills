"""ÖĞREN-4 d2 (★ 11:58 v): kaynağı yalnız ad listesi/.mcp.json olan kalem RET; ad listesi kalemi zip'teki gerçek skill'e çözülür.
  python -X utf8 .claude/ogren4/test_v2.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import v2

assert v2.kaynak_ret(".kos/kopru/claudeai_adlar.json")
assert v2.kaynak_ret(r"C:\Users\pc\.claude\plugins\cache\x\1.0.0\.mcp.json")
assert v2.kaynak_ret(".kos/kopru/ogren/katalog-son.jsonl")
assert not v2.kaynak_ret(r"C:\Users\pc\.claude\skills\video-tarama\SKILL.md")
z = v2.coz("orbit-card")  # remotion-video-paket alt skill'i (TALIMAT/REFERANS)
assert z and z.endswith("/skills/orbit-card/") and "orbit" in v2.metin("orbit-card", z), z
assert v2.coz("adobe-paket").endswith("adobe-paket/SKILL.md")  # paket kalemi: yalnız kendi yönlendirici SKILL.md'si
assert v2.coz("gstack-make-pdf").endswith("make-pdf\\SKILL.md")
assert v2.coz("yok-boyle-bir-skill-xyz") is None
# d3 (★ 12:58 ii): kayıt JSON'u/katalog satırı kaynağı RET değil `kaynak_yetersiz` kartı; kanıt = o dosyanın yolu
assert v2.kaynak_ret(r"C:\Projeler\omer-skills\.kos\kopru\envanter\omni_models_api.json") and v2.kaynak_ret(r"C:\Users\pc\.claude.json")
k = v2.yetersiz_kart("markitdown", r"C:\Users\pc\.claude.json")
assert k["dogrulandi"] == "kaynak_yetersiz" and k["mekanizma"] == "kaynak yetersiz" and k["kanit"] == r"C:\Users\pc\.claude.json", k
assert v2.yetersiz_kart("x", r"C:\x\SKILL.md") is None
o = Path(__file__).parent / "v2-ornek.tsv"
if o.is_file():  # kayıt-kaynaklı satırların hepsi birlestir'de kaynak_yetersiz kartı olur (RET değil)
    assert all(v2.yetersiz_kart(*s.split("\t")[::3]) for s in o.read_text(encoding="utf-8").splitlines() if v2.kaynak_ret(s.split("\t")[3]))
print("test_v2 tamam")
