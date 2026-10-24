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
    return {"ANTHROPIC_BASE_URL": URL, "ANTHROPIC_MODEL": MODEL, "ANTHROPIC_SMALL_FAST_MODEL": MODEL,
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": MODEL, "ANTHROPIC_DEFAULT_SONNET_MODEL": MODEL, "ANTHROPIC_DEFAULT_OPUS_MODEL": MODEL}


def env_kur(env):
    """Kimlik temizliği: abonelik/API anahtarı ve OMNIROUTE_KEY'i çıkarır; tek kimlik ANTHROPIC_AUTH_TOKEN=OMNIROUTE_KEY."""
    k = anahtar(env)
    if not k:
        raise RuntimeError("OMNIROUTE_KEY yok")
    yeni = {a: d for a, d in env.items() if not SIZINTI.match(a)}
    yeni.update(ayar_env())
    yeni["ANTHROPIC_AUTH_TOKEN"] = k
    return yeni
