"""ENVANTER-2 madde 2: bilinen 30 iş → beklenen araçlardan biri ilk 3'te, oran ≥ %90."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import katalog_ara  # noqa: E402

ISLER = [
    ("Postgres tablosunda deadlock hatası alıyorum", {"db-kilitlenme"}),
    ("yavaş SQL sorgusunu hızlandır, query plan oku", {"db-sorgu-optimize", "db-indeks-danismani"}),
    ("EF Core migration oluştur", {"dn-efcore-migration"}),
    ("xUnit testi yaz C#", {"dn-xunit-test-yazar"}),
    ("flaky test neden ara sıra kırılıyor", {"qa-flaky-avci"}),
    ("Playwright ile uçtan uca test", {"qa-e2e-playwright", "qa-playwright"}),
    ("repo geçmişinde sızmış sır tara gitleaks", {"sec-gitleaks-gecmis", "sec-sir-tarayici", "gitleaks"}),
    ("JWT doğrulama güvenliğini incele", {"sec-jwt-denetci", "sec-jwt-oturum"}),
    ("SQL injection açığı bul", {"sec-injection-denetci"}),
    ("ffmpeg ile video kırp ve sıkıştır", {"vid-ffmpeg-donusturucu", "ffmpeg"}),
    ("youtube videosunu altyazıdan özetle", {"ara-youtube-ozet", "vid-video-ozetle"}),
    ("yt-dlp ile video indir", {"vid-ytdlp-indirme", "yt-dlp"}),
    ("Blender sahnesini GLB olarak dışa aktar three.js için", {"bl-glb-disa-aktar"}),
    ("Blender UV açma, gerilen dokular", {"bl-uv-acma"}),
    ("n8n iş akışı tasarla", {"otm-n8n-akis-tasarimi"}),
    ("cron ile zamanlanmış görev kur", {"otm-zamanlanmis-gorev"}),
    ("merge çakışmasını çöz", {"git-cakisma-cozucu"}),
    ("commit mesajı yaz diff'ten", {"git-commit-mesaji"}),
    ("git bisect ile hatalı commit bul", {"git-bisect-rehber"}),
    ("changelog sürüm notları yaz", {"dok-degisiklik-gunlugu"}),
    ("Word docx rapor üret", {"dok-docx-uretici"}),
    ("PDF'i markdown'a çevir", {"dok-markitdown-donusum"}),
    ("karanlık mod ekle", {"fe-karanlik-mod"}),
    ("form tasarımı doğrulama hata mesajları", {"fe-form-tasarimci"}),
    ("Kubernetes probe ve resource limit ayarla", {"ops-k8s-is-yuku"}),
    ("terraform modülü yaz", {"ops-terraform"}),
    ("A/B test örneklem büyüklüğü", {"urn-ab-test-istatistik"}),
    ("zaman serisi tahmini satış", {"ml-zaman-serisi"}),
    ("lisans kontrolü harici repo kodu almadan önce", {"ara-lisans-kontrol"}),
    ("React Native liste takılıyor performans", {"mob-rn-performans"}),
]


def test_ilk3_orani():
    if not katalog_ara.KATALOG.exists():
        pytest.skip("katalog yok: python tools/katalog_yenile.py")
    satirlar = [__import__("json").loads(s) for s in katalog_ara.KATALOG.read_text(encoding="utf8").splitlines()]
    kayip = [(q, [o["ad"] for o in katalog_ara.ara(q, satirlar=satirlar, n=3)])
             for q, beklenen in ISLER
             if not beklenen & {o["ad"] for o in katalog_ara.ara(q, satirlar=satirlar, n=3)}]
    assert len(ISLER) - len(kayip) >= 0.9 * len(ISLER), kayip


def test_genislet_tr_en():
    assert "security" in katalog_ara.genislet("güvenlik açığı")
    assert katalog_ara.kelimeler("Çakışma-Çözücü") == ["cakisma", "cozucu", "cakis~", "cozuc~"]
