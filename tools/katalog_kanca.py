"""KATALOG-KANCA-1: UserPromptSubmit kancası — zor işte (≥2 alan, alan dışı ya da "hangi araç" sorusu) katalog adaylarını
<katalog> eki olarak bağlama koyar; rutin tek alanlı işte, kısa/slash/devam yanıtında ve hata/zaman aşımında hiçbir şey yazmaz.
Dayanak: ENVANTER-6 (zor 12 işte ön-enjeksiyon kör puan 72/72 vs 66/72, jeton −%16) · ENVANTER-2 (rutin 30 işte kazanç 0).
stdin: kanca olay JSON'u (prompt, session_id) → stdout: hookSpecificOutput.additionalContext JSON'u ya da boş. Çıkış hep 0.
"""
import hashlib
import json
import re
import sys
import tempfile
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # repo: tools/ · canlı: ~/.claude/skills/yetenek-getir/
import katalog_ara  # noqa: E402

DIZIN = Path(tempfile.gettempdir()) / "katalog-kanca"  # oturum başına gösterilen iş karmaları
SURE, TAVAN, ADAY, TABAN, KISA = 1.5, 12000, 40, 3, 40
SON = "Bu işte uygun araçları yalnız bu listeden seç; ek katalog sorgusu yapma."
YANIT = re.compile(r"^(devam|evet|tamam|ok|okay|olur|peki|aynen|hayir|onay|onayla|dur|bekle|yes|no|go on|continue)\b")
SORU = re.compile(r"\bhangi (arac|skill|ajan|mcp|plugin|eklenti|kutuphane|cli)|\bwhich (tool|skill|agent|library|plugin|mcp)"
                  r"|\bne kullan(ay|ma|sa)")
# katlanmış (ASCII, küçük harf) metinde kelime başı kalıpları; departman-diger alt alanları ayrı sayılır (oyun ≠ hukuk)
ALAN = {
    "frontend": r"landing|arayuz|\bui\b|css|tailwind|react(?! native)|bilesen|site|web|seo\b|three|tarayici|webassembly|wasm|frontend|razor",
    "backend": r"api\b|api'|backend|\.net|dotnet|c#|asp\.?net|blazor|websocket|mikroservis",
    "veri": r"veritaban|sql|postgres|mysql|supabase|sqlite|mongo|redis|ef core|migration|rls\b|csv|veri hatt|etl\b|graf|neo4j",
    "guvenlik": r"guvenlik|owasp|jwt|kimlik dogrula|yetki|kvkk|gdpr|kisisel veri|maskele|hile|pentest|zafiyet|anahtar|izin|sir(lar|ri)?\b",
    "test": r"test|xunit|pytest|playwright|\bqa\b|e2e|benchmark|performans",
    "git": r"\bgit\b|commit|pull request|\bpr\b|rebase|\bci\b|pipeline|yayin|surum",
    "inceleme": r"kod incele|review|kalite denetim|statik|audit",
    "belge": r"docx|pptx|pdf|xlsx|excel|sunum|slayt|belge|dokuman|blog|surum not",
    "ajan": r"skill|plugin|eklenti|hook|kanca|mcp\b|ajan|agent|jeton|token|baglam|maliyet|oturum|claude|prompt",
    "izleme": r"log\b|log dosya|gozlemlen|alarm|grafana|prometheus|izleme|sentry|pano",
    "bulut": r"kubernetes|k8s|docker|aws\b|azure|gcp\b|vps\b|dns\b|sunucu|barindir|olcekle|terraform|helm\b|felaket|dagitim|alan adi",
    "medya": r"video|\bses\b|ses kayd|podcast|kurgu|klip|ffmpeg|altyazi",
    "gorsel": r"gorsel|resim|fotograf|goruntu isle|logo\b",
    "3d": r"blender|\b3d\b|glb\b|gltf|mesh|rig\b|rig'",
    "oyun": r"oyun|unity|godot|unreal|\bmod\b|mod paket",
    "mobil": r"mobil|\bios\b|android|\bapk\b|react native|flutter|app store|google play|magaza|apns|push",
    "ml": r"regresyon|siniflandir|\brag\b|llm|yapay zeka|makine ogren|\bml\b",
    "hukuk": r"sozlesme|hukuk|kira\b|kira |dava\b|fesih",
    "finans": r"finans|kdv|muhasebe|mutabakat|fatura|yatirim|banka",
    "pazarlama": r"pazarlama|sosyal medya|reklam|lansman|e-posta|eposta|kampanya|pazar arastir|analitik",
    "otomasyon": r"otomasyon|\bbot\b|slack|n8n|zamanla|cron|beti[kg]|toplu|kazi|discord",
    "gomulu": r"stm32|esp32|gomulu|firmware|uart|arduino|mikrodenetleyici",
}
ALAN = {k: re.compile(r"\b(?:" + v + ")") for k, v in ALAN.items()}


def katla(s):
    return s.translate(katalog_ara.TR).lower()  # önce translate: "İ".lower() birleşik nokta bırakır


def alanlar(istem):
    m = katla(istem)
    return {k for k, r in ALAN.items() if r.search(m)}


def tetik(istem):
    m = katla(istem).strip()
    if len(m) <= KISA or m.startswith("/") or YANIT.match(m):
        return False
    return len(alanlar(istem)) != 1 or bool(SORU.search(m))


def ek(istem):
    sonuc = katalog_ara.aday(istem[:1000], ADAY, taban=TABAN)
    while True:  # tavanı aşarsa sondan kırp (aday sırası BM25 + tür tabanı)
        e = f"<katalog>\n{katalog_ara.metin(sonuc)}\n</katalog>\n{SON}"
        if len(e) <= TAVAN or len(sonuc) <= 5:
            return e
        sonuc = sonuc[:-5]


def isle(girdi):
    try:
        olay = json.loads(girdi.decode("utf8"))
        istem, sid = olay["prompt"], re.sub(r"[^\w-]", "", str(olay.get("session_id", "")))[:64] or "yok"
        if not isinstance(istem, str) or not tetik(istem):
            return ""
        karma = hashlib.sha1(katla(istem)[:500].encode("utf8")).hexdigest()[:16]
        kayit = DIZIN / f"{sid}.txt"
        if kayit.exists() and karma in kayit.read_text(encoding="utf8").split():
            return ""
        sonuc = []
        t = threading.Thread(target=lambda: sonuc.append(ek(istem)), daemon=True)
        t.start()
        t.join(SURE)
        if not sonuc:  # zaman aşımı ya da katalog hatası: istem engellenmez, sessiz geç
            return ""
        DIZIN.mkdir(parents=True, exist_ok=True)
        with kayit.open("a", encoding="utf8") as f:
            f.write(karma + "\n")
        return json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": sonuc[0]}}, ensure_ascii=False)
    except Exception:
        return ""


if __name__ == "__main__":
    cikti = isle(sys.stdin.buffer.read())
    if cikti:
        sys.stdout.buffer.write(cikti.encode("utf8"))
