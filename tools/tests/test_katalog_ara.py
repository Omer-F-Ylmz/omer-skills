"""ENVANTER-2 madde 2: bilinen 30 iş → beklenen araçların hepsi eşik sonucunda (geri çağırma ≥ %95)."""
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
    ("Playwright ile uçtan uca test", {"qa-e2e-playwright", "qa-playwright", "playwright", "playwright-cli"}),
    ("repo geçmişinde sızmış sır tara gitleaks", {"sec-gitleaks-gecmis", "sec-sir-tarayici", "gitleaks"}),
    ("JWT doğrulama güvenliğini incele", {"sec-jwt-denetci", "sec-jwt-oturum"}),
    ("SQL injection açığı bul", {"sec-injection-denetci"}),
    ("ffmpeg ile video kırp ve sıkıştır", {"vid-ffmpeg-donusturucu", "ffmpeg"}),
    ("youtube videosunu altyazıdan özetle", {"ara-youtube-ozet", "vid-video-ozetle"}),
    ("yt-dlp ile video indir", {"vid-ytdlp-indirme", "youtube-downloader"}),
    ("Blender sahnesini GLB olarak dışa aktar three.js için", {"bl-glb-disa-aktar"}),
    ("Blender UV açma, gerilen dokular", {"bl-uv-acma"}),
    ("n8n iş akışı tasarla", {"otm-n8n-akis-tasarimi", "n8n-mcp"}),
    ("cron ile zamanlanmış görev kur", {"otm-zamanlanmis-gorev"}),
    ("merge çakışmasını çöz", {"git-cakisma-cozucu"}),
    ("commit mesajı yaz diff'ten", {"git-commit-mesaji", "writing-commit-messages"}),
    ("git bisect ile hatalı commit bul", {"git-bisect-rehber"}),
    ("changelog sürüm notları yaz", {"dok-degisiklik-gunlugu"}),
    ("Word docx rapor üret", {"dok-docx-uretici", "example-skills:docx"}),
    ("PDF'i markdown'a çevir", {"dok-markitdown-donusum", "markitdown-mcp", "markitdown"}),
    ("karanlık mod ekle", {"fe-karanlik-mod", "ui-design:dark-mode-design"}),
    ("form tasarımı doğrulama hata mesajları", {"fe-form-tasarimci"}),
    ("Kubernetes probe ve resource limit ayarla", {"ops-k8s-is-yuku"}),
    ("terraform modülü yaz", {"ops-terraform", "terraform-skill"}),
    ("A/B test örneklem büyüklüğü", {"urn-ab-test-istatistik", "marketing-skills:ab-testing"}),
    ("zaman serisi tahmini satış", {"ml-zaman-serisi"}),
    ("lisans kontrolü harici repo kodu almadan önce", {"ara-lisans-kontrol"}),
    ("React Native liste takılıyor performans", {"mob-rn-performans"}),
]


def test_geri_cagirma():
    """Beklenen araçların HEPSİ sonuçta (geri çağırma ≥ %95); kesinlik alt sınırı = beklenen/sonuç, raporlanır."""
    if not katalog_ara.KATALOG.exists():
        pytest.skip("katalog yok: python tools/katalog_yenile.py")
    satirlar = [__import__("json").loads(s) for s in katalog_ara.KATALOG.read_text(encoding="utf8").splitlines()]
    bulunan = toplam = sonuc_say = 0
    kayip = []
    for q, beklenen in ISLER:
        adlar = {o["ad"] for o in katalog_ara.ara(q, satirlar=satirlar)}
        bulunan += len(beklenen & adlar)
        toplam += len(beklenen)
        sonuc_say += len(adlar)
        kayip += [(q, b) for b in beklenen - adlar]
    print(f"geri çağırma {bulunan}/{toplam} · ort. sonuç {sonuc_say / len(ISLER):.1f} · kesinlik >= {bulunan / sonuc_say:.2f}")
    assert bulunan >= 0.95 * toplam, kayip


def test_skill_kopyasi_guncel():
    """yetenek-getir klasöründeki betik + katalog, kaynakla aynı (CC kurulumu ve claude.ai zip'i repo yoluna bağlı değil)."""
    kok = Path(__file__).resolve().parents[2]
    for kaynak in ("tools/katalog_ara.py", "docs/katalog/yetenek.tsv", "docs/katalog/yetenek.jsonl"):
        k = kok / kaynak
        assert k.read_bytes() == (kok / "skills" / "yetenek-getir" / k.name).read_bytes(), "python tools/katalog_yenile.py"


def test_genislet_tr_en():
    assert "security" in katalog_ara.genislet("güvenlik açığı")
    assert katalog_ara.kelimeler("Çakışma-Çözücü") == ["cakisma", "cozucu", "cakis~", "cozuc~"]
