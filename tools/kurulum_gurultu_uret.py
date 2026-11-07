"""GURULTU-KUR-1 uretici: docs/envanter/kurulum-kuyruk.tsv + tools/kurulum_gurultu.ps1. Kurulum yapmaz."""
import io
from pathlib import Path

K = Path(__file__).resolve().parent.parent
HF = "HF"
# kalem | resmi kaynak | yontem | boyut | lisans | son | sinif | not | ps satiri ('' = yorum satiri uretilir)
S = [
 ("Cloudflare/clef", "huggingface.co/Cloudflare/clef (GitHub'da yok)", "HF-agirlik", "51.21 GiB", "Apache-2.0", "2026-10-30", "OMER-SOR", ">2GB",
  "# OMER-SOR (51.21 GiB): hf download Cloudflare/clef"),
 ("Cloudflare/clef-flash", "huggingface.co/Cloudflare/clef-flash", "HF-agirlik", "17.77 GiB", "Apache-2.0", "2026-10-30", "OMER-SOR", ">2GB",
  "# OMER-SOR (17.77 GiB): hf download Cloudflare/clef-flash"),
 ("Tijo2000/clef-decision-demo", "github.com/ajmontalbano/clef-decision-demo (Tijo2000 hesabi yok)", "KLON", "50 KB", "MIT", "2026-10-30", "KLON", "sahip adi duzeltildi",
  "Kur5Klon 'clef-decision-demo' 'ajmontalbano/clef-decision-demo'"),
 ("convaiinnovations/laya", "huggingface.co/convaiinnovations/laya (GitHub'da yok)", "HF-agirlik", "2.21 GiB", "Apache-2.0", "2026-10-03", "OMER-SOR", ">2GB",
  "# OMER-SOR (2.21 GiB): hf download convaiinnovations/laya"),
 ("axolotl", "github.com/axolotl-ai-cloud/axolotl", "KLON", "70 MB", "Apache-2.0", "2026-11-06", "KLON", "pip kurulumu CUDA/Linux odakli; Windows'ta yalniz klon",
  "Kur5Klon 'axolotl' 'axolotl-ai-cloud/axolotl'"),
 ("langchain-ai", "github.com/langchain-ai/langgraph (TEK repo: video ajan orkestrasyonu baglami)", "KLON", "520 MB", "MIT", "2026-11-06", "KLON", "org -> langgraph",
  "Kur5Klon 'langchain-ai (langgraph)' 'langchain-ai/langgraph'"),
 ("HKUDS", "github.com/HKUDS/LightRAG (TEK repo: V2RIVnGCy74 videosu arac listesinde LightRAG)", "KLON", "115 MB", "MIT", "2026-11-05", "KLON", "org -> LightRAG",
  "Kur5Klon 'HKUDS (LightRAG)' 'HKUDS/LightRAG'"),
 ("multica-ai/andrej-karpathy-skills", "github.com/multica-ai/andrej-karpathy-skills", "SKILL", "20 KB", "YOK (lisanssiz)", "2026-04-20", "SKILL", "lisans yok: engel degil, raporda",
  "Kur5Skill 'andrej-karpathy-skills' 'multica-ai/andrej-karpathy-skills' 'skills'  # lisans: none"),
 ("ilabai/3dcodeverse", "github.com/gaoypeng/3dcodeverse (ilabai hesabi yok)", "KLON", "45 MB", "Apache-2.0", "2026-11-04", "KLON", "sahip adi duzeltildi",
  "Kur5Klon '3dcodeverse' 'gaoypeng/3dcodeverse'"),
 ("Heroic Labs (Nakama)", "github.com/heroiclabs/nakama", "KLON", "160 MB", "Apache-2.0", "2026-11-06", "KLON", "Go sunucu; derleme/Docker Omer'in",
  "Kur5Klon 'Nakama' 'heroiclabs/nakama'"),
 ("nano-pdf", "pypi.org/project/nano-pdf 0.2.1 (github.com/gavrielc/Nano-PDF)", "UV", "kucuk", "MIT", "2025-12-03", "UV", "",
  "Kur5Uv 'nano-pdf' 'nano-pdf'"),
 ("himalaya", "github.com/pimalaya/himalaya v2.2.1 (winget manifesti yok)", "INDIR", "19 MB", "Apache-2.0", "2026-11-06", "INDIR", "skills/himalaya zaten kurulu; bu CLI ikilisi",
  "Kur5Indir 'himalaya' 'https://github.com/pimalaya/himalaya/releases/download/v2.2.1/himalaya.x86_64-windows.zip'"),
 ("skills/manim-video", "~/.claude/skills/manim-video (+affaan-m-, nousresearch-)", "SKILL", "-", "-", "-", "ZATEN", "yerel skill dizinleri var",
  "# ZATEN: ~/.claude/skills/manim-video, affaan-m-manim-video, nousresearch-manim-video"),
 ("nanochat", "github.com/karpathy/nanochat", "KLON", "2.5 MB", "MIT", "2026-09-07", "KLON", "model indirmez",
  "Kur5Klon 'nanochat' 'karpathy/nanochat'"),
 ("storm-research/SKILL", "github.com/openwhat007/storm-research (MIT; SevenBaylor kopyasi lisanssiz)", "SKILL", "kucuk", "MIT", "2026-06-24", "SKILL", "",
  "Kur5Skill 'storm-research' 'openwhat007/storm-research' ''"),
 ("Paperclip Agents", "github.com/paperclipai/paperclip", "KLON", "480 MB", "MIT", "2026-11-07", "KLON", "",
  "Kur5Klon 'Paperclip' 'paperclipai/paperclip'"),
 ("Spacedrive", "github.com/spacedriveapp/spacedrive v0.4.3 (winget manifesti yok)", "INDIR", "86 MB msi", "Apache-2.0", "2026-11-06", "UYGULAMA", "uygulama: yorum, Omer msi'yi calistirir",
  "# UYGULAMA (86 MB msi, Omer calistirir): Kur5Indir 'Spacedrive' 'https://github.com/spacedriveapp/spacedrive/releases/download/v0.4.3/Spacedrive-windows-x86_64.msi'"),
 ("Typst", "winget Typst.Typst (winget-pkgs manifesti dogrulandi)", "WINGET", "kucuk", "Apache-2.0", "2026-11-06", "WINGET", "-Sistem ister",
  "Kur5Winget 'Typst' 'Typst.Typst'"),
 ("MegaTTS3 (ses turu adayi)", "huggingface.co/ByteDance/MegaTTS3", "HF-agirlik", "3.98 GiB", "Apache-2.0", "2025-04-04", "OMER-SOR", "indirme YOK, yalniz boyut; >2GB",
  "# OMER-SOR (3.98 GiB, ses turu adayi, indirilmedi): hf download ByteDance/MegaTTS3"),
]

tsv = ["kalem\tkaynak\tyontem\tboyut\tlisans\tson_guncelleme\tsinif\tnot"]
tsv += ["\t".join(r[:8]) for r in S]
(K / "docs/envanter/kurulum-kuyruk.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")

ust = (K / "tools/kurulum_omer2_onsoz.ps1").read_text(encoding="utf-8-sig").splitlines()[:69]
ust = "\n".join(ust)
ust = ust.replace("# KURULUM-5B (uretici: tools/kurulum_omer2_uret.py)", "# GURULTU-KUR-1 (uretici: tools/kurulum_gurultu_uret.py)")
ust = ust.replace("kurulum-omer2-sonuc.tsv", "kurulum-gurultu-sonuc.tsv")
ust = ust.replace('"__KLON__"', '"$env:USERPROFILE\\Downloads\\kurulum-gurultu\\klon"')
ust = ust.replace('"$env:USERPROFILE\\Downloads\\kurulum5b"', '"$env:USERPROFILE\\Downloads\\kurulum-gurultu"')
gov = [f"# --- {r[0]} | {r[6]} | {r[4]} | {r[3]}\n{r[8]}" for r in S]
(K / "tools/kurulum_gurultu.ps1").write_bytes(("﻿" + ust + "\n" + "\n".join(gov) + "\n").encode("utf-8"))
from collections import Counter
print(Counter(r[6] for r in S))
