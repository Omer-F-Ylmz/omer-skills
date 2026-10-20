"""SLASH-ÖĞREN kapı: held-out 10 görevde katalogdan doğru komutu seçme (betik hakem). 1 `claude -p` (haiku, araçsız)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
GOREV = [  # (görev, beklenen ad) — katalog satırlarındaki sözcüklerle birebir örtüşmeyen anlatımlar
    ("Testler kırmızı ve nedenini bilmiyorum, yama yazmadan önce ne yapayım?", "systematic-debugging"),
    ("Bu repoda ödeme modülü hangi dosyalara bağlı, haritayı çıkar.", "graphify"),
    ("Müşteri için yeni bir açılış sayfası tasarlayacağım.", "frontend-craft"),
    ("Yarın birleştireceğim pull request'in diff'ini gözden geçir.", "code-review"),
    ("Yeni giriş formuna SQL enjeksiyonu açığı var mı bakılsın.", "security-reviewer"),
    ("Anthropic SDK ile prompt önbellekleyen bir servis yazacağım.", "claude-api"),
    ("Bu iş hem veritabanı hem arayüz hem CI; hangi araçlar gerekir bilmiyorum.", "plan-kur"),
    ("Altyazısız bir Instagram videosunda ne konuşulduğunu öğrenmek istiyorum.", "watch"),
    ("Önce başarısız test yazıp sonra en az kodla geçireceğim.", "test-driven-development"),
    ("Kendi yazdığım skill'in kalitesini ölçüp iyileştirmek istiyorum.", "skill-creator"),
]

if __name__ == "__main__":
    katalog = (KOK / "skills/yetenek-getir/reference/slash-katalog.md").read_text(encoding="utf-8")
    istem = (katalog + "\n\nHer görev için katalogdan TEK en uygun skill/komut adını seç (yalnız ad, `:` önekini ve `/`'ı at). "
             'Yanıt yalnız JSON dizisi: ["ad1", ... 10 öğe].\n' + "\n".join(f"{i + 1}. {g}" for i, (g, _) in enumerate(GOREV)))
    p = subprocess.run([shutil.which("claude"), "-p", "--output-format", "json", "--model", "haiku", "--tools", "", "--disable-slash-commands",
                        "--setting-sources", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--no-session-persistence"],
                       input=istem, capture_output=True, text=True, encoding="utf-8", cwd=str(KOK), timeout=300)
    yanit = json.loads(p.stdout)["result"]
    secim = json.loads(re.search(r"\[.*\]", yanit, re.S).group(0))
    dogru = sum(1 for s, (_, b) in zip(secim, GOREV) if s.split(":")[-1].strip("/ ") == b)
    print(f"{dogru}/{len(GOREV)} = %{100 * dogru // len(GOREV)}", secim)
