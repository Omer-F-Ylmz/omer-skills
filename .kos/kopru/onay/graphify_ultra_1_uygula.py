r"""GRAPHIFY-ULTRA-1 G6 onay betiği: (1) ~/.agents/skills/graphify 0.9.57 → paket sürümü (`graphify install --platform agents`,
yalnız skill; AGENTS.md'ye dokunmaz) (2) skills/graphify-desktop/SKILL.md → CC marketplace kopyası.

Kullanım: python C:\Projeler\omer-skills\.kos\kopru\onay\graphify_ultra_1_uygula.py          # yedek + uygula
          python C:\Projeler\omer-skills\.kos\kopru\onay\graphify_ultra_1_uygula.py --kuru   # canlıya DOKUNMAZ: yapılacakları + sürüm/sha yazar
          python C:\Projeler\omer-skills\.kos\kopru\onay\graphify_ultra_1_uygula.py --geri   # son yedekleri geri koy
"""
import hashlib, shutil, subprocess, sys, tempfile, time
from pathlib import Path

AJAN = Path.home() / ".agents" / "skills" / "graphify"
KAYNAK = Path(r"C:\Projeler\omer-skills\skills\graphify-desktop\SKILL.md")
HEDEF = Path.home() / ".claude" / "plugins" / "marketplaces" / "omer-skills" / "skills" / "graphify-desktop" / "SKILL.md"
YEDEK = Path(__file__).parent / "yedek"


def sha(y):
    return hashlib.sha256(Path(y).read_bytes()).hexdigest()[:12]


def surum():
    return (AJAN / ".graphify_version").read_text(encoding="utf-8").strip()


def main(a):
    sys.stdout.reconfigure(encoding="utf-8")
    if "--geri" in a:
        ys, ms = sorted(YEDEK.glob("graphify_ultra_1-agents-*")), sorted(YEDEK.glob("graphify_ultra_1-desktop-*.md"))
        if ys:
            shutil.rmtree(AJAN)
            shutil.copytree(ys[-1], AJAN)
            print("geri agents:", ys[-1].name, "→", surum())
        if ms:
            shutil.copyfile(ms[-1], HEDEF)
            print("geri desktop:", ms[-1].name, "→", sha(HEDEF))
        return None if ys or ms else print("yedek yok")
    if "--kuru" in a:
        print(f"KURU agents: {AJAN} {surum()} → `graphify install --platform agents` (cwd geçici dizin)")
        return print(f"KURU desktop: {HEDEF}: sha {sha(HEDEF)} → {sha(KAYNAK)}")
    YEDEK.mkdir(exist_ok=True)
    t = time.strftime("%Y%m%d-%H%M%S")
    shutil.copytree(AJAN, YEDEK / f"graphify_ultra_1-agents-{t}")
    shutil.copyfile(HEDEF, YEDEK / f"graphify_ultra_1-desktop-{t}.md")
    once = surum()
    subprocess.run(["graphify", "install", "--platform", "agents"], cwd=tempfile.mkdtemp(), check=True, capture_output=True)
    print(f"agents: {once} → {surum()}")
    once = sha(HEDEF)
    shutil.copyfile(KAYNAK, HEDEF)
    print(f"desktop: sha {once} → {sha(HEDEF)}")


if __name__ == "__main__":
    main(sys.argv[1:])
