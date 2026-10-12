# IG-40-KUR aday doğrulama yönergesi (alt ajan)

Girdi: `C:/Projeler/omer-skills-wt/igkur/.claude/igkur/parcaN.tsv` (anahtar · ad · tur · link · gonderi · iddia). Kaynak raporlar: `C:/Projeler/omer-skills/docs/video-tarama/2026-10-12-ig-<gonderi>.md` (## URL'ler, ## Kurulum/komutlar, ## Kareden okunanlar bölümlerinde link/repo adı ipucu olabilir; Grep -n ile ara, Read dar aralık).

Her satır için doğrula ve ÇIKTI dosyasına (`sonucN.tsv`, UTF-8, LF, başlık satırıyla) tek satır yaz. Sütunlar (sekme ile):
`anahtar	ad	tur	link	gonderi	iddia	var_mi	lisans	bakim	windows	guvenlik	izin	baglam	bizde	karar	devir	gerekce	kurulum	hesap`

- link/var_mi: gerçek repo/sayfa (gh search repos / gh api repos/o/r / brave-search / WebSearch / mcp-fetch). Ad belirsizse rapordaki kareden okunan metin + hesap adıyla ara. Bulunamazsa var_mi=hayır.
- lisans: SPDX (gh api repos/o/r --jq .license.spdx_id). bakim: `★<yıldız> push:<YYYY-MM-DD> arşiv:<e/h>`.
- windows: evet / hayır / wsl / belirsiz (+ kısa neden).
- guvenlik: YALNIZ karar KUR/UYARLA olan yeni (bizde yok) git repoları için: `gh repo clone o/r <T>/<slug> -- --depth 1` (T=`C:/Users/pc/AppData/Local/Temp/igkur`, her repo kendi boş klasörü; repo içinden hiçbir betik/derleme ÇALIŞTIRMA) →
  `gitleaks dir <d> --no-banner --redact -f json -r <d>.gl.json` · `semgrep scan --config p/security-audit --metrics=off --quiet --json -o <d>.sg.json <d>` · skill/plugin ise `skillspector scan <d> --no-llm --format json --output <d>.ss.json`.
  Kurulum betiklerini (install.sh/.ps1, package.json postinstall/preinstall, setup.py) oku: ağdan indirip çalıştırma, ~/.ssh / env okuma, telemetri var mı. Yaz: `gl:<n> sg:<n ERROR> ss:<HIGH+CRIT> betik:<temiz|not>`. Taranmadıysa neden.
- izin: istediği kapsam (dosya yazma, ağ, shell, tarayıcı, hesap token'ı). baglam: skill/MCP ise yaklaşık bağlam maliyeti (SKILL.md kelime / araç sayısı).
- bizde: `C:/Projeler/omer-skills-wt/igkur/.claude/igkur/envanter.txt` (skill/plugin/mcp/npm/uv adları), `C:/Projeler/omer-skills/docs/kurulumlar/adaylar/*.md` ve `docs/kurulumlar/kacan-karar*.tsv` (önceki kararlar — Grep -l ile ad ara, büyük dosyaları okuma), `C:/Projeler/omer-skills/docs/kaynak/awesome/` ve `skills/` (omer-kutuphaneler, awesome-rehber). Yaz: `kurulu:<ad>` / `kısmen:<ad>` / `yok` / `önceki-karar:<dosya>`. "Zaten var" ise ikisinin iyi yanını 1 cümleyle karşılaştır; bizde eksik bir özellik varsa karar UYARLA (ne alınacağı gerekce'de).
- karar (hedef: bulunanların %90–95'i KUR/UYARLA; REF/RED istisna):
  - KUR = gerçek, lisans izinli (MIT/Apache/BSD/ISC/MPL/CC0/Unlicense…), Windows'ta çalışır, güvenlik temiz. Zaten kuruluysa da KUR (bizde=kurulu:…, kurulum=`kurulu`). Hesap/anahtar isteyen servis de KUR (hesap sütunu doldurulur).
  - UYARLA = lisans yok/kısıtlı, Windows'ta çalışmıyor ama mekanizma alınabilir, ya da bizdeki karşılıkta eksik iyi yan var → kendi skill/aracımıza mekanizma (kod kopyası YOK). gerekce'de alınacak mekanizma + hedef dosya/skill.
  - REF = kurulacak bir şey değil (genel ürün: Claude Code/Cursor/ChatGPT; salt bilgi sayfası; anlamsız/genel terim).
  - RED = yalnız: kötü amaçlı, lisans yasak ve mekanizma alınamaz, ölü (yok/arşiv ve yerine geçen yok), Windows'ta çalışmaz ve uyarlanamaz. gerekce zorunlu.
- devir: Blender/3D → `blender` · animasyon/efekt/hareket → `animasyon` · site/UI/tasarım/görsel prompt → `tasarim` · Fable/düşünme tarzı/ajan protokolü → `fable` · model yönlendirici/router → `router` · değilse `-`. Devir satırlarında güvenlik taraması yapma (ilgili ajan yapar), var_mi/lisans/link yeter.
- kurulum: KUR için tam komut (CC tarafı): `claude plugin marketplace add o/r` + `claude plugin install p@m` · `claude mcp add -s user <ad> -- <komut>` · skill: `skill-klonla o/r <alt-yol>` · `npm i -g <pkg>` · `uv tool install <pkg>`. claude.ai'ye gidecekse sonuna ` | claudeai:ucuncu-taraf` (3. taraf skill zip'i) ya da ` | claudeai:kendi` (UYARLA ile bizim yazacağımız). Kurulu ise `kurulu`.
- hesap: anahtar/hesap gerekiyorsa `site · ücretsiz kota · neden`; yoksa `-`. Anahtar DEĞERİ hiçbir yerde yazılmaz; env değeri basma.

Kurallar: hiçbir şeyi KURMA/kaldırma (yalnız araştır, klonla, tara); pencere/tarayıcı açma; telif alıntı ≤15 kelime; ücretli API çağrısı yok. Hücrelerde sekme/yeni satır yok, `|` yerine `/`.
Bitince ana ajana yalnız şunu dön (≤5 satır): yazılan dosya yolu, satır sayısı, karar dağılımı (KUR/UYARLA/REF/RED), devir sayısı, taranan repo sayısı + bulgu olan repolar.
