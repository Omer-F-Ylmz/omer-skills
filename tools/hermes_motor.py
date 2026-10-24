"""HERMES-KUR-1 PARÇA 5c: ajan_sira motor=hermes. `claude -p` yerine koşar: istemi stdin'den alır, `hermes chat -Q -q` ile ücretsiz modelde çalıştırır,
claude -p JSON sözleşmesinin tek satırını basar (is_kaydi / bos_kosu aynen çalışır). Ek argümanlar (--session-id ...) yok sayılır."""
import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EXE = KOK / "araclar/hermes/Scripts/hermes.exe"
HOME = KOK / "araclar/hermes-home"
MODEL = "nvidia/nemotron-3.5-lightning:free"  # OpenRouter :free slug'ları değişir; HERMES_MODEL ile ezilir (güncel liste: openrouter.ai/api/v1/models, fiyat 0)
SURE = 1500


def hazir():
    return EXE.exists() and bool(os.environ.get("OPENROUTER_API_KEY"))


def sonuc_json(rc, metin):
    ok = rc == 0 and bool(metin.strip())
    # shortcut: Hermes -Q tur sayısı vermez; boş olmayan çıktıya 2 yazılır, boş-koşu denetimini anahtar kelime (görev adı) yapar
    return json.dumps({"type": "result", "subtype": "success" if ok else f"error_rc{rc}", "result": metin.strip(), "num_turns": 2 if ok else 0,
                       "total_cost_usd": 0, "usage": {"input_tokens": 0, "output_tokens": len(metin) // 4}})  # ASCII-güvenli: cp1254 konsolda │ gibi karakterler basılamaz


def main():
    istem = sys.stdin.buffer.read().decode("utf-8")
    dosya = Path(tempfile.gettempdir()) / f"hermes_istem_{os.getpid()}.md"
    dosya.write_text(istem, encoding="utf-8")  # uzun istem argv'ye sığmaz (WinError 206) → dosya yolu
    komut = shlex.split(os.environ["HERMES_KOMUT"], posix=False) if os.environ.get("HERMES_KOMUT") else [str(EXE)]
    argv = [*komut, "chat", "-Q", "-q", f"Görev dosyasını oku ve görevi eksiksiz yap, bitince sonuç metninde görev adını ve KABUL/DUR satırını yaz: {dosya}",
            "--provider", "openrouter", "-m", os.environ.get("HERMES_MODEL", MODEL), "--max-turns", "60"]
    env = {**os.environ, "HERMES_HOME": str(HOME), "PYTHONUTF8": "1"}
    try:
        r = subprocess.run(argv, capture_output=True, env=env, timeout=SURE, creationflags=0x08000000)
        rc, metin = r.returncode, r.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        rc, metin = 124, ""
    finally:
        dosya.unlink(missing_ok=True)
    print(sonuc_json(rc, metin), flush=True)
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
