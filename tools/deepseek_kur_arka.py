import hashlib
import json
import os
import shutil
import subprocess
import time
import zipfile
from pathlib import Path

KOK = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored")
MODEL = KOK / "model"
LOG = KOK / "kurulum_arka.log"
DURUM = KOK / "kurulum_durum.json"
REPO = "Abiray/DeepSeek-V4.1-Flash-1017-Uncensored-GSQ-RCO-IQ2_XXS-GGUF"
LLAMA_DIR = Path.home() / ".local" / "llama.cpp"
CURL = r"C:\Windows\System32\curl.exe"
ALT_SINIR_GB = 30
BEKLENEN = {
    "DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ2_XXS-00001-of-00006.gguf": "f356f198561f56df36f7ab92d7238a926646d76de992c34f15bcb939a5f529b9",
    "DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ2_XXS-00002-of-00006.gguf": "db021c117306070573a8aba333f34f9c47ee757a1072aaacc0cab7bf4c737862",
    "DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ2_XXS-00003-of-00006.gguf": "5c6de54009714a6996985f86553348e5d8e0d5ece7f64a89558e2f53d90bfa76",
    "DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ2_XXS-00004-of-00006.gguf": "706de34f9c252234cd349081b3b76bf69dc77677ac8d006f7d4538558ba49e87",
    "DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ2_XXS-00005-of-00006.gguf": "85e29c00f0d5616de05d20b96e367ed9eb3ba20ed958c860da899dad8c9f7a8e",
    "DeepSeek-V4.1-Flash-Engram-IQ4_NL.gguf": "3dac4c54893ad7aa89103c0028500eadc78e74112cef3a2930a97e67dc9fb4f3",
    "mmproj-DeepSeek-V4.1-Flash-1017-BF16.gguf": "0fdc4b7693f287e9665940cf42bd39c546ffe4f0def89c569d7d0e45d60d2df1",
}


def yaz(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


def durum(asama, **ek):
    veri = {"asama": asama, "zaman": time.strftime("%Y-%m-%d %H:%M:%S"), **ek}
    DURUM.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")


def bos_gb():
    return shutil.disk_usage("C:\\").free / 2**30


def curl(url, hedef=None, devam=False):
    komut = [CURL, "-sS", "-L", "--fail", "--retry", "5", "--retry-delay", "10", "-A", "deepseek-kur"]
    tok = os.environ.get("HF_TOKEN")
    if tok and "huggingface.co" in url:
        komut += ["-H", "Authorization: Bearer " + tok]
    if hedef:
        komut += ["-o", str(hedef)]
        if devam:
            komut += ["-C", "-"]
    komut.append(url)
    r = subprocess.run(komut, capture_output=True)
    if r.returncode not in (0, 33):
        raise RuntimeError("curl %s: %s" % (r.returncode, r.stderr.decode("utf-8", "replace")[-400:]))
    return r.stdout


def llama_bul():
    for p in LLAMA_DIR.rglob("llama-server.exe"):
        return str(p)
    return shutil.which("llama-server")


def llama_zip_kur():
    rels = json.loads(curl("https://api.github.com/repos/ggml-org/llama.cpp/releases?per_page=10"))
    rel = next(r for r in rels if r["tag_name"].startswith("b") and any("win-cuda-12.4-x64" in a["name"] for a in r["assets"]))
    yaz("surum %s" % rel.get("tag_name"))
    secilen = [a for a in rel["assets"] if a["name"].endswith("bin-win-cuda-12.4-x64.zip")]
    yaz("varliklar %s" % [a["name"] for a in secilen])
    LLAMA_DIR.mkdir(parents=True, exist_ok=True)
    for a in secilen:
        hedef = LLAMA_DIR / a["name"]
        curl(a["browser_download_url"], hedef)
        with zipfile.ZipFile(hedef) as z:
            z.extractall(LLAMA_DIR)
        hedef.unlink()
    return rel.get("tag_name")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blok in iter(lambda: f.read(16 * 2**20), b""):
            h.update(blok)
    return h.hexdigest()


def main():
    durum("basladi", bos_gb=round(bos_gb()))
    if bos_gb() - 251 < ALT_SINIR_GB and not MODEL.exists():
        durum("ENGEL-disk", bos_gb=round(bos_gb()))
        return

    llama = llama_bul()
    if not llama:
        durum("llama.cpp zip kuruluyor")
        llama_zip_kur()
        llama = llama_bul()
    if not llama:
        durum("HATA-llama.cpp kurulamadi")
        return
    r = subprocess.run([llama, "--version"], capture_output=True, text=True, errors="replace")
    surum = (r.stdout + r.stderr).strip()[-300:]
    yaz("llama %s | %s" % (llama, surum))

    MODEL.mkdir(parents=True, exist_ok=True)
    for i, ad in enumerate(BEKLENEN, 1):
        hedef = MODEL / ad
        if hedef.exists() and hedef.with_suffix(".ok").exists():
            continue
        for deneme in range(1, 8):
            durum("indiriliyor", dosya=ad, sira="%d/%d" % (i, len(BEKLENEN)), deneme=deneme,
                  bos_gb=round(bos_gb()), llama=llama, llama_surum=surum)
            if bos_gb() < ALT_SINIR_GB:
                durum("ENGEL-disk-alt-sinir", bos_gb=round(bos_gb()))
                return
            try:
                curl("https://huggingface.co/%s/resolve/main/%s" % (REPO, ad), hedef, devam=True)
                break
            except Exception as e:
                yaz("indir hata %s %r" % (ad, e))
                time.sleep(60)
        else:
            durum("HATA-indirme", dosya=ad)
            return
        durum("sha256", dosya=ad)
        if sha(hedef) != BEKLENEN[ad]:
            yaz("SHA UYUSMAZ %s" % ad)
            durum("HATA-sha256", dosya=ad)
            return
        hedef.with_suffix(".ok").write_text("ok")
        yaz("SHA OK %s" % ad)

    engram = MODEL / "DeepSeek-V4.1-Flash-Engram-IQ4_NL.gguf"
    shard6 = MODEL / "DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ2_XXS-00006-of-00006.gguf"
    if not shard6.exists():
        os.link(engram, shard6)
    durum("TAMAM", bos_gb=round(bos_gb()), llama=llama, llama_surum=surum)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        yaz("ISTISNA %r" % e)
        durum("ISTISNA", hata=repr(e))
