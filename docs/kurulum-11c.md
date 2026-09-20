# KURULUM-11c — 11b kalanı + anahtar hijyeni · 21 Eyl 2026

## Sabit satırlar

- **PATH-FIX (21 Eyl)** — HKCU Path REG_SZ→ExpandString, 15→12 girdi (3 boş + sondaki
  `;` silindi), tırnak üç kaynakta da yok, HKLM'ye dokunulmadı. Kök neden: geçmişte
  `setx Path` / `SetEnvironmentVariable(...,'User')`. **KURAL:** Path'e bu iki yol bir
  daha kullanılmaz, yalnız `Set-ItemProperty -Type ExpandString`.
- **claude-design KALIR** — CC: aktif MCP · Desktop: karşılığı Design / Design System
  artifact türü (ayrı sunucu değil, bu yüzden Desktop sayımında görünmez).

## K0 — context7 tekilleştirme (tarifden sapma)

Ölçüm (salt-okunur, değer basılmadan):

- Canlı Desktop config **15 stdio** tanımı içeriyor ve içinde **tek** `context7` var:
  `cmd /c npx -y @upstash/context7-mcp --api-key %CONTEXT7_API_KEY%`.
- `c1492263` dizesi hiçbir Desktop veri dizininde **yok**: `config.json`,
  `Local Storage/leveldb`, `IndexedDB`, `extensions-blocklist.json`,
  `AppData\Local\Claude`, `Claude-Data`, `Claude-3p`.

**Sonuç:** ikinci tanım yerel dosyadan gelmiyor → hesap tarafı (claude.ai → Settings →
Connectors) **uzak bağlayıcı**. Desktop aynı adlı iki sunucuyu görünce birine
`-c1492263` soneki ekliyor. Config düzenlenerek kaldırılamaz.

**Karar:** yerel stdio tanımı kalır (kuru test: `initialize` + `tools/list` **OK, 2 araç,
Context7 4.0.5, 0.3 sn**). Uzak bağlayıcının kaldırılması tek UI adımı → Ömer'in sırası.
Config'e dokunulmadı; CC `mcpServers` hash'i değişmedi (17 sunucu, `874d34b9…c836bc7`).

## K7 — anahtar hijyeni

**Kalıcı kural** `~/.claude/CLAUDE.md` satır 19'a yazıldı (yer açmak için 18. satırdaki
iki kural birleştirildi): ortam değişkeni DEĞERİ hiçbir komutla yazdırılmaz; varlık
kontrolü yalnız boolean; `reg query` / `Get-ChildItem Env:` / `env|grep` yasak.

### K7a — tarama (gitleaks detect --no-git --redact, 4 hedef)

| Hedef | Durum | Bulgu |
|---|---|---|
| `~/.claude/projects` — 11b oturum `.jsonl` (49 dosya, 176 MB) | VAR | **52** |
| `~/.claude-mem` (32 MB, db + corpora + logs) | VAR | **0** |
| `~/.claude/shell-snapshots` (224 KB) | VAR | **0** |
| `~/.claude/history.jsonl` (116 KB) | VAR | **0** |

52 bulgunun dağılımı: `C--Projeler-omer-skills` **6** (kural: `github-oauth`),
`subagents` 14, `Garajim` 32 (`jwt` ağırlıklı — **kapsam dışı**, ayrı projenin kendi kodu).

Anahtar **adları** (değer yazılmadan), omer-skills 11b transkriptlerinde düz değerle:

| Anahtar adı | Eşleşme | Yenileme adresi |
|---|---|---|
| `BRAVE_API_KEY` | 2 | api-dashboard.search.brave.com → API Keys |
| `CONTEXT7_API_KEY` | 2 | context7.com → Dashboard → API Keys |
| `STITCH_API_KEY` | 2 | stitch.withgoogle.com → Settings → API |
| `GITHUB_TOKEN` | 2 | github.com/settings/tokens |

### K7b — temizlik: **YAPILAMADI (izin)**

Redaksiyon betiği hazırdı (yedek al → `KEYNAME=<değer>` ve `gh[pousr]_…` desenlerini
`[REDACTED-11c]` ile değiştir → yerine yaz), ancak `~/.claude/projects` altındaki oturum
transkriptlerine yazma **izin sınıflandırıcısı tarafından engellendi**. Dosyalara
dokunulmadı. Sebep: canlı oturum geçmişinin yeniden yazılması hassas işlem sayılıyor.
Çözüm Ömer'in onayını gerektirir — ayrıntı raporda.

### K7d — yenileme

Yukarıdaki 4 anahtar yenilenmeli. **Yenileme yapılmadı** (tarif gereği); bu belge
Ömer'in henüz yenilemediği varsayımıyla yazıldı.

## K5 — claude-mem

**Proje envanteri (tek SQL sorgusu, `claude-mem.db`):**

| Tablo | Proje dağılımı |
|---|---|
| `observations` | `omer-skills` 379 |
| `session_summaries` | `omer-skills` 31 |
| `sdk_sessions` | `omer-skills` 26 |
| `tool_uses` | `omer-skills` 911 |

Gözlem aralığı: 2026-09-19T19:37 → 2026-09-20T21:33.

**Boş korpuslar silindi:** `corvano.corpus.json`, `divisima.corpus.json` (ikisi de 0 gözlem).
Kalan: `omer-skills.corpus.json` (335 gözlem, ~160k token).

**Kayıt neden yalnız omer-skills'te?** Hook kapsamı **değil** — claude-mem hook'ları
global `~/.claude/settings.json`'da tanımlı, proje bazlı değil; proje adı eşleşmesi de
doğru çalışıyor (omer-skills doğru adla kayıtlı). Dört tablonun dördünde de tek proje
var: gözlemci 19 Eyl kurulumundan bu yana yalnız omer-skills oturumlarını işlemiş.
20 Eyl'de koşan Garajim oturumu (`a22bb3f9`) hiçbir tabloda yok — **işlenmeme nedeni
kanıtlanmadı**, 11d'ye kalır.

## K1 — yeni kanıt (teşhis denemesi YOK)

20 Eyl, Desktop **yeniden başlatılMADAN** açılan yeni sohbette: sayım 22 sunucu ve
`omniroute` listede **yok**. omniroute 11b/K0'da config'ten silinmişti; araç listesi
uygulama açılışında donsaydı hâlâ görünürdü.

→ Liste, config yazımından **sonra** tazelenmiş. "Bayat liste" hipotezi **zayıf**;
`puppeteer` + `brave-search` gerçekten gelmiyor. Sonraki adım 11d'de kurgulanır.

**obsidian** — `~/.claude/ide/` boş, sabit port yazılamıyor → **YAPISAL**, kapandı.
Tekrar denenmez; Obsidian açıkken lock oluşursa 11d'de bakılır.

## K2 — 7 CLI için Desktop paketi

Karar: **7/7 (b) yöntem skill'i**. Hiçbiri (a) olmadı; sessizce düşen kalem yok.

| Araç | Karar | Kanıt |
|---|---|---|
| graphify | (b) | uv-tool venv 145 MB — 30 MB sınırını aşıyor |
| agent-reach | (b) | çekirdek işlev (Jina/yt-dlp/gh) ağ isteyen fetch; sandbox ağsız |
| skill-ui | (b) | repo 1.1 GB; `mirror`/`upload` GitHub ağına yazıyor |
| playwright-cli | (b) | sarmalayıcı küçük ama tarayıcı ikilileri `playwright install` ile ayrıca iniyor |
| rtk | (b) | `duman_claudeai.py` "tamam" döndü, ama ikili Windows PE32+ — gerçek sandbox Linux |
| semgrep | (b) | uv-tool venv 333 MB — sınırı çok aşıyor |
| gitleaks | (b) | boyutça (a) adayı (22.5 MB), kapı "tamam" (exit 0, 8.30.1) verdi; ikili PE32+ → sandbox Linux'ta koşmaz |

**rtk ve gitleaks için önemli not:** ikisi de `tools/duman_claudeai.py` kapısından
fiilen geçti, ama geçiş **Windows'ta koşmaktan** kaynaklanıyor. Scriptin kendi
belgelediği hedef sandbox Linux (`/mnt/skills`); Windows PE32+ ikili orada
çalıştırılamaz. Bu yüzden geçiş gerçek kanıt sayılmadı ve karar (b)'ye çevrildi.

Paketler: `dist/yukle-11c/<araç>-desktop.zip` (7 adet, 665–881 B).
`python tools/skill_denetim.py dist/yukle-11c` → **0 hata · 0 CRLF · 0 ad çakışması**, exit 0.
Her SKILL.md başlığında "bu araç Claude Code'da koşar, Desktop'ta koşmaz" uyarısı var.
