r"""HOOK-3-devam: gsd-core v1.16.0'ın (MIT) kırpılmış yerel marketplace çatalı.
  python tools/gsd_catal.py <gsd-core git klonu> <hedef> [--ref v1.16.0] [--olcum]
Liste maliyeti (B2 aile kalıbı): 72 skill + 72 komut + 64 ajan → tek `gsd` skill'i; alt komutlar skills/gsd/alt/<ad>.md,
ajanlar ajanlar/<ad>.md (auto-discovery dışı, general-purpose + rol dosyası). İçerik birebir korunur.
Hook'lar: yalnız TUT (değer ↔ gecikme kararı rapor hook3.md); ağ çağıran gsd-check-update ve her araçta koşan bekçiler dışarıda.
--olcum: hedef/gsd-core klonun gsd-core'una junction olur → ensure-canonical-path no-op, canlı ~/.claude/gsd-core'a yazılmaz."""
import json, re, shutil, subprocess, sys, tarfile, io
from pathlib import Path

SURUM = "1.16.0-omer.1"
TUT = {("SessionStart", "gsd-ensure-canonical-path"), ("PreToolUse", "gsd-write-guard"),
       ("PreToolUse", "gsd-secret-read-guard"),
       ("PostToolUse", "gsd-read-injection-scanner"), ("FileChanged", "gsd-config-reload")}
DAR = {"gsd-read-injection-scanner": "WebFetch|WebSearch"}  # yerel Read her çağrıda taranmaz; dış içerik taranır
ACIKLAMA = ("GSD çok fazlı proje yönetimi: yeni proje, .planning/ROADMAP.md + STATE.md, faz planla/yürüt/doğrula, "
            "oturumlar arası ilerleme. /gsd <alt> [arg]. Tek seferlik SPEC/uygulama planı, araştırma ya da tek dosyalık kod işi için değil.")


def _acik(md):
    m = re.search(r'^description:\s*"?(.*?)"?\s*$', md, re.M)
    return m.group(1) if m else ""


def catal(k: Path, kaynak_sha: str):
    alt = k / "skills" / "gsd" / "alt"; alt.mkdir(parents=True)
    satirlar = []
    for d in sorted(p for p in (k / "skills").iterdir() if p.name != "gsd"):
        md = (d / "SKILL.md").read_text(encoding="utf-8")
        ad = d.name.removeprefix("gsd-")
        (alt / f"{ad}.md").write_text(md, encoding="utf-8")
        satirlar.append(f"- {ad} — {_acik(md)}")
        shutil.rmtree(d)
    (k / "skills" / "gsd" / "SKILL.md").write_text(f"""---
name: gsd
description: "{ACIKLAMA}"
argument-hint: "<alt> [argümanlar]"
---
GSD Core v1.16.0 (open-gsd, MIT) — {len(satirlar)} alt komut tek girişte. Bu skill'in temel dizini = D (Base directory).
1. Alt komutu seç (kullanıcı `/gsd <alt>` dediyse o; yoksa aşağıdaki listeden işe uyan) ve `D/alt/<alt>.md` dosyasını Read et; oradaki talimatı izle, `$ARGUMENTS` = alt adından sonraki argümanlar.
2. `@~/.claude/gsd-core/...` satırları otomatik eklenmez: Read ile oku (yol yoksa `D/../../gsd-core/...`).
3. Talimat `subagent_type="gsd-X"` ajanı isterse: Agent(subagent_type="general-purpose", prompt="Önce D/../../ajanlar/gsd-X.md dosyasını Read et ve oradaki rolü uygula.\\n\\n" + asıl prompt).

Alt komutlar:
""" + "\n".join(satirlar) + "\n", encoding="utf-8")
    shutil.rmtree(k / "commands", ignore_errors=True)
    (k / "agents").rename(k / "ajanlar")
    pj = json.loads((k / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    pj.pop("commands", None); pj["version"] = SURUM
    (k / ".claude-plugin" / "plugin.json").write_text(json.dumps(pj, indent=2, ensure_ascii=False), encoding="utf-8")
    mj = json.loads((k / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    mj["name"] = "gsd-core-omer"; mj["plugins"][0]["version"] = SURUM
    (k / ".claude-plugin" / "marketplace.json").write_text(json.dumps(mj, indent=2, ensure_ascii=False), encoding="utf-8")
    hj = json.loads((k / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    yeni = {}
    for e, L in hj["hooks"].items():
        for m in L:
            ad = m["hooks"][0]["command"].split("/hooks/")[1].split(".")[0]
            if (e, ad) in TUT:
                yeni.setdefault(e, []).append({**m, "matcher": DAR[ad]} if ad in DAR else m)
    (k / "hooks" / "hooks.json").write_text(json.dumps({**hj, "hooks": yeni}, indent=2), encoding="utf-8")
    (k / "ATIF.md").write_text(f"""# Atıf
Bu dizin open-gsd/gsd-core (https://github.com/open-gsd/gsd-core) v1.16.0 sürümünün ({kaynak_sha}) değiştirilmiş kopyasıdır. Lisans: MIT (LICENSE, telif open-gsd).
Değişiklikler (omer-skills tools/gsd_catal.py): skills/* → skills/gsd/alt/*.md (tek giriş), commands/ silindi (skill kopyası), agents/ → ajanlar/,
hooks.json yalnız {sorted(a for _, a in TUT)}; gsd-read-injection-scanner matcher → WebFetch|WebSearch. Sürüm {SURUM}.
""", encoding="utf-8")


def main(a):
    src, hedef = Path(a[0]), Path(a[1])
    ref = a[a.index("--ref") + 1] if "--ref" in a else "v1.16.0"
    sha = subprocess.run(["git", "-C", str(src), "rev-parse", "--short", f"{ref}^{{commit}}"], capture_output=True, text=True, check=True).stdout.strip()
    shutil.rmtree(hedef, ignore_errors=True); hedef.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", str(src), "archive", "--format=tar", ref], capture_output=True, check=True).stdout
    tarfile.open(fileobj=io.BytesIO(tar)).extractall(hedef, filter="data")
    catal(hedef, sha)
    if "--olcum" in a:
        shutil.rmtree(hedef / "gsd-core")
        subprocess.run(["cmd", "/c", "mklink", "/J", str(hedef / "gsd-core"), str(src / "gsd-core")], capture_output=True, check=True)
    print(f"çatal {sha} → {hedef}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
