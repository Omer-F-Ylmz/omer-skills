"""UCRETSIZ-MOTOR-1: kuyruk ajanını Claude aboneliği yerine yerel OmniRoute'taki ücretsiz Claude-dışı modelle koşturur.
claude CLI aynı bayraklarla; ANTHROPIC_BASE_URL → OmniRoute (/v1/messages), model = ücretsiz combo. Abonelik/API kimlikleri
ortamdan temizlenir; tek kimlik OMNIROUTE_KEY'dir (yalnız alt sürecin ortamına, hiçbir dosyaya yazılmaz)."""
import os
import re

URL = "http://127.0.0.1:20128"
MODEL = "ucretsiz-ozet2"  # 24 Eki canlı ölçüm: Write+Read+Bash görevi KABUL (nemotron-3-ultra :free); ucretsiz-groq aynı görevde 429 verdi
SIZINTI = re.compile(r"^(ANTHROPIC_|CLAUDE_CODE_OAUTH|CLAUDE_CODE_USE_|CLAUDE_CODE_SKIP_|AWS_BEARER|OMNIROUTE_KEY$)")
ZOR = re.compile(r"mimari|güvenlik (düzelt|açığ)|inatçı|kalite kapısı", re.I)
KOLAY = re.compile(r"paketle|paketleme|rapor|kanıt|doğrula|katalog|kart|muaf|zip|belge|log tara", re.I)


# UCRETSIZ-MOTOR-2-DEVAM A: boş koşu/hata sonrası haiku'ya değil sıradaki ücretsiz sağlayıcıya (OmniRoute'ta görünenler; Mistral/Cloudflare/SambaNova OmniRoute'ta yok → atlandı)
ZINCIR = ["hermes", "ucretsiz-ozet2", "openrouter/nvidia/nemotron-3.5-lightning:free", "ucretsiz-groq", "gemini/gemini-3.7-flash", "ollama/qwen3.5:9b"]
AKTIF = None  # ajan_sira başlatmadan önce seçili zincir modelini koyar
AG_RE = re.compile(r"API Error|\b50[234]\b|connection_error|getaddrinfo|ECONNRESET|ETIMEDOUT", re.I)
AG_BEKLE_DK = (2, 5, 10)


def model():
    return AKTIF or MODEL


def sonraki(adim, hermes_hazir=True):
    """Zincirde adim'dan sonraki ücretsiz basamak (hermes hazır değilse atlanır); bitti → None."""
    for i in range(adim + 1, len(ZINCIR)):
        if ZINCIR[i] != "hermes" or hermes_hazir:
            return i
    return None


def ag_hatasi(j):
    """UCRETSIZ-MOTOR-2-DEVAM B2: subtype=success olsa da sonuç ağ/ağ geçidi hatasıysa model başarısı değil, AĞ-HATASI."""
    return bool(j.get("api_error_status") in (502, 503, 504) or AG_RE.search((j.get("result") or "")[:400]) and j.get("num_turns", 0) <= 1)


def ag_var(ana="openrouter.ai"):
    import socket
    try:
        socket.getaddrinfo(ana, 443)
        return True
    except OSError:
        return False


def anahtarlar(ad, istem):
    """UCRETSIZ-MOTOR-2: görevin ad/rapor yolu/commit öneki — sonuç metninde en az biri geçmeli."""
    ad = re.sub(r"(-r|-a\d+|-z\d+)+$", "", ad)  # yeniden deneme ekleri: ajan görevin asıl adını yazar
    return [ad.lower()] + [x.lower() for x in re.findall(r"rapor/[\w.-]+\.md", istem)] + \
           [x.lower() for x in re.findall(r'Commit "([^"]+)"', istem)]


def bos_kosu(j, anahtar_listesi):
    """UCRETSIZ-MOTOR-2: subtype success yetmez — selamlama/boş yanıt = BOŞ-KOŞU (işlem yok, anahtar yok)."""
    sonuc = (j.get("result") or "").lower()
    return j.get("num_turns", 0) < 2 or not any(a in sonuc for a in anahtar_listesi)


def hatirlat(ad, istem):
    """UCRETSIZ-MOTOR-2: ~190k bağlamda zayıf model görevi kaçırdı → görev ilk satırı sonda yinelenir (son mesaj en güçlü)."""
    ilk = (istem.strip().splitlines() or [ad])[0][:300]
    return (f"\n\n[GÖREV — YUKARIDAKİ OTURUM BAĞLAMI ARKA PLANDIR, SOHBET ETME] '{ad}': {ilk}\n"
            f"Araç çağırarak bu işi yap; bitince sonuç metninde '{ad}' adını ve KABUL/DUR satırını yaz.")


def anahtar(env=None):
    """OMNIROUTE_KEY: ortam, yoksa HKCU. Değeri hiçbir çıktıya yazılmaz."""
    env = os.environ if env is None else env
    if env.get("OMNIROUTE_KEY"):
        return env["OMNIROUTE_KEY"]
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, "OMNIROUTE_KEY")[0]
    except (ImportError, OSError):
        return None


def hazir(env=None):
    return bool(anahtar(env))


def kolay(ad, metin):
    """Görev başlığı (ilk satır) + ad: zor işaret → False; kolay işaret → True; ikisi de yoksa False (Haiku'dan başlar)."""
    baslik = f"{ad} {metin.strip().splitlines()[0] if metin.strip() else ''}".replace("İ", "i")
    return not ZOR.search(baslik) and bool(KOLAY.search(baslik))


def ayar_env():
    """--settings profil dosyasına birleşecek env (anahtar YOK): profildeki olası ANTHROPIC_* ezilir, arka plan çağrıları da ücretsiz modele gider."""
    m = model()
    return {"ANTHROPIC_BASE_URL": URL, "ANTHROPIC_MODEL": m, "ANTHROPIC_SMALL_FAST_MODEL": m,
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": m, "ANTHROPIC_DEFAULT_SONNET_MODEL": m, "ANTHROPIC_DEFAULT_OPUS_MODEL": m}


def env_kur(env):
    """Kimlik temizliği: abonelik/API anahtarı ve OMNIROUTE_KEY'i çıkarır; tek kimlik ANTHROPIC_AUTH_TOKEN=OMNIROUTE_KEY."""
    k = anahtar(env)
    if not k:
        raise RuntimeError("OMNIROUTE_KEY yok")
    yeni = {a: d for a, d in env.items() if not SIZINTI.match(a)}
    yeni.update(ayar_env())
    yeni["ANTHROPIC_AUTH_TOKEN"] = k
    return yeni
