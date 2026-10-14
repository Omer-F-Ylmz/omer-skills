"""ENVANTER-KULLAN-1: kurulu araçları gerçek komutla yokla → probe.tsv (araç · yol · kanıt satırı)."""
import json, os, shutil, subprocess, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
CIKTI = Path(__file__).with_name("probe.tsv")
izinli = json.loads((KOK / "tools/cc-kopru/kopru.json").read_text(encoding="utf-8"))["izinli"]
ALLOW = [k for k in izinli if not k.startswith("_")]
EKSTRA = ["ollama", "lms", "yt-dlp", "tesseract", "blender", "comfy", "magick", "ffprobe", "whisper",
          "llama-cli", "llama-server", "docker", "nvidia-smi", "pwsh", "deno", "pnpm", "cargo", "go",
          "java", "rg", "jq", "qmd", "context-mode", "claude", "codex", "gemini", "lighthouse", "omniroute",
          "aria2c", "exiftool", "pandoc", "sqlite3", "duckdb", "ruff", "pytest", "markitdown", "docling"]
# bazı araçlar --version'ı bilmiyor; sıra ile denenir
BAYRAK = {"ffmpeg": ["-version"], "ffprobe": ["-version"], "gitleaks": ["version"], "whisper-cli": ["--help"],
          "tesseract": ["--version"], "nvidia-smi": ["--query-gpu=name,memory.total,memory.used,utilization.gpu", "--format=csv,noheader"],
          "ollama": ["list"], "lms": ["ls"], "go": ["version"], "java": ["-version"], "dotnet": ["--version"],
          "skill-ui": ["--help"], "strix": ["--help"], "video": ["--help"], "crv": ["--help"], "jev": ["--help"],
          "headroom": ["--help"], "pixeljury": ["--help"], "summarize": ["--help"], "mcp-video-analyzer": ["--help"],
          "claude-usage": ["--help"], "agent-reach": ["--help"], "playwright-cli": ["--help"], "blender": ["-b", "--version"],
          "magick": ["-version"]}


def kos(arg, t=25):
    try:
        p = subprocess.run(arg, capture_output=True, text=True, timeout=t, encoding="utf-8", errors="replace",
                           stdin=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        s = (p.stdout or "") + (p.stderr or "")
        satir = [x.strip() for x in s.splitlines() if x.strip()]
        return p.returncode, satir
    except Exception as e:  # zaman aşımı / çalıştırılamaz
        return -1, [type(e).__name__ + ": " + str(e)[:80]]


def main():
    satirlar = []
    for ad in ALLOW + [e for e in EKSTRA if e not in ALLOW]:
        yol = shutil.which(ad)
        if not yol:
            satirlar.append(f"{ad}\t{'allow' if ad in ALLOW else 'ekstra'}\tYOK\t-")
            continue
        rc, s = kos([yol] + BAYRAK.get(ad, ["--version"]))
        kanit = " | ".join(s[:2])[:160] if s else f"(bos çıktı rc={rc})"
        satirlar.append(f"{ad}\t{'allow' if ad in ALLOW else 'ekstra'}\t{yol}\trc={rc} {kanit}")
        print(ad, rc, file=sys.stderr)
    CIKTI.write_text("\n".join(satirlar) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
