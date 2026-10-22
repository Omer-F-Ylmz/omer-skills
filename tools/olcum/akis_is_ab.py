"""AJAN-AKIS-1 ÖLÇÜM (gerçek iş A/B): 2 küçük gerçek-biçimli iş (hata ayıklama · özellik ekleme) × 2 kol (çekirdeksiz · çekirdekli) = 4 `claude -p --model sonnet` çağrısı (TAVAN 4).
Her iş geçici dizinde kurulur, başarı = pytest çıkışı 0; ölçülen: geçti, tur, maliyet $, toplam giriş jetonu.
python tools/olcum/akis_is_ab.py → .kos/kopru/akis/is_ab.json"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ajan_cekirdek as AC  # noqa: E402

NW = 0x08000000
IS1 = {  # hata ayıklama: iki hata (ayraç + sınır)
    "takvim.py": "def gun_farki(a, b):\n    \"\"\"'YYYY-AA-GG' iki tarih arası gün farkı (b - a).\"\"\"\n    ya, ma, ga = map(int, a.split('/'))\n    yb, mb, gb = map(int, b.split('-'))\n    return (yb * 365 + mb * 30 + gb) - (ya * 365 + ma * 30 + ga)\n",
    "test_takvim.py": "from takvim import gun_farki\n\n\ndef test_ay_icinde():\n    assert gun_farki('2025-03-01', '2025-03-11') == 10\n\n\ndef test_ay_asan():\n    assert gun_farki('2025-01-31', '2025-02-01') == 1\n\n\ndef test_yil_asan():\n    assert gun_farki('2024-12-31', '2025-01-01') == 1\n",
    "ISTEM": "test_takvim.py başarısız. Hatayı bul ve takvim.py'yi düzelt; testleri değiştirme. Bitirmeden pytest'i koş.",
}
IS2 = {  # özellik: spec dosyasını okuyup uygula
    "SPEC.md": "rapor(satirlar) -> str\n- satirlar: 'ad;tutar' biçiminde metin listesi (tutar tam sayı, TL).\n- Geçersiz satır (';' yok ya da tutar sayı değil) atlanır.\n- Çıktı: önce 'TOPLAM: <n> TL', sonra tutara göre AZALAN sırayla 'ad: tutar' satırları (eşitte ada göre A-Z).\n- Hiç geçerli satır yoksa çıktı tam olarak 'BOŞ'.\n",
    "rapor.py": "# rapor(satirlar) burada yazılacak\n",
    "test_rapor.py": "from rapor import rapor\n\n\ndef test_normal():\n    assert rapor(['b;5', 'a;5', 'c;9']) == 'TOPLAM: 19 TL\\nc: 9\\na: 5\\nb: 5'\n\n\ndef test_gecersiz_atlanir():\n    assert rapor(['x', 'y;abc', 'z;3']) == 'TOPLAM: 3 TL\\nz: 3'\n\n\ndef test_bos():\n    assert rapor(['x']) == 'BOŞ'\n",
    "ISTEM": "SPEC.md'yi oku, rapor.py'de rapor()'u uygula; test_rapor.py geçmeli. Testleri değiştirme.",
}


def calistir(is_, kol):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for ad, ic in is_.items():
            if ad != "ISTEM":
                (d / ad).write_text(ic, encoding="utf-8")
        istem = (AC.onek() if kol == "sonra" else "") + is_["ISTEM"]
        env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
        p = subprocess.run(["claude", "-p", "--model", "claude-sonnet-5-5", "--output-format", "json", "--max-turns", "15", "--tools", "Read,Edit,Write,Bash",
                            "--permission-mode", "bypassPermissions", "--setting-sources", ""], input=istem, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600, creationflags=NW, cwd=d, env=env)
        try:
            j = json.loads(p.stdout)
        except ValueError:
            return dict(kol=kol, hata="json")
        u = j.get("usage") or {}
        t = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=d, capture_output=True, text=True, creationflags=NW)
        return dict(kol=kol, gecti=t.returncode == 0, tur=j.get("num_turns"), usd=round(j.get("total_cost_usd", 0), 3),
                    giris=u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0), cikis=u.get("output_tokens", 0))


if __name__ == "__main__":
    sonuc = {}
    for ad, is_ in (("hata-ayiklama", IS1), ("ozellik", IS2)):
        for kol in ("once", "sonra"):
            sonuc[f"{ad}/{kol}"] = calistir(is_, kol)
            print(ad, kol, sonuc[f"{ad}/{kol}"], flush=True)
    out = KOK / ".kos/kopru/akis/is_ab.json"
    out.write_text(json.dumps(dict(sonuc=sonuc, zaman=time.strftime("%Y-%m-%d %H:%M")), ensure_ascii=False, indent=1), encoding="utf-8")
