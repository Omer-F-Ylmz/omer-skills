---
name: departman-belge
description: "Belge müdürü: docx/pptx/pdf/xlsx, rapor ve doküman üretim sırası. Sunum, PDF, proje dokümantasyonu ya da metin düzeltme işinde oku."
---

# Departman: belge — iş sırası

Katalog: `docs/departmanlar/belge.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.

## Adımlar
1. **Tür** — proje dokümanı `document-generate` / `project-documenter`; karar kaydı `documentation-and-adrs`; ortak yazım `doc-coauthoring`.
2. **Biçim** — markdown → PDF `make-pdf`; diyagram `diagram`; sunum `wowerpoint`.
3. **Dil** — AI izi temizliği `humanizer`, yazım kılavuzu `writing-guidelines`.
4. **Yayın sonrası** — `document-release`.

## Kapılar
- Belge koddan türetilir; kodla çelişen iddia yazılmaz.

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- phoenix-docs-research (3): notebooklm, phoenix-research-pipeline, project-documenter · `C:/Users/pc/.claude/plugins/cache/phoenix-security/phoenix-docs-research/1.0.0/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:dok-adr-yazar: a technical choice must be recorded
ajan:dok-api-dokumani
ajan:dok-cevirmen-teknik: docs must be bilingual
ajan:dok-degisiklik-gunlugu: releasing a version
ajan:dok-docx-uretici
ajan:dok-pdf-uretici: kaçın: fatura → invoice/fatura-kutusu
ajan:dok-pptx-sunum
ajan:dok-rapor-ozetleyici
ajan:dok-sorun-giderme-rehberi: support questions repeat
ajan:dok-tablo-duzenle
ajan:dok-teknik-teklif
ajan:dok-toplanti-notu: notes need cleaning up
ajan:dok-xlsx-tablo
ajan:otm-bildirim-yonlendirme: notifications are noisy
ajan:otm-dosya-isleme-botu: many files need the same operation
ajan:oyn-oyun-motoru-script: implementing a mechanic
fatura-kutusu: fatura/invoice PDF, saat bazlı danışmanlık
humanizer: prose with AI tells: forced contrasts, staged openers
jev: ıcı birden çok öğeyi sınıflamak, etiketlemek ya da
### yalnız Claude Code
ai-labs-paket: Genel amaçlı skill derlemesi: geliştirme, pazarlama, belge
benchmark-methodology: Use after competitive-platform-analysis has produced a tiered competitor
connections-optimizer: レビュー優先の整理、フォロー/追加の推薦、ユーザーの実際の声で書かれたチャネル別ウォームアウトリーチのドラフトを通じて、ユーザーのXとLinkedInネットワークを再編成します。フォローリストを整理したい、現在の優先事項に向けて成長したい、または高品質な関係を中心にソーシャルグラフのバランスを取り直したい場合に使用します。
constraint-specification: Defining output format, length, tone, and content boundaries
crosspost: the user wants to distribute content across social
discernment-nudge: asked a trivial how-to or simple lookup, wants
financial-router: Routes finance: Bigdata/RavenPack, US fundamentals/yfinance, A-share news/policy, sector
game-recon: oyun modlanabilir mi, motor tespiti, modcu topluluğu
i18n-sync: adding keys or languages, updating source copy, or
incremental-implementation: implementing any feature or change that touches more
li-dm: the user says "write a connection request", "DM
lifekernel-second-brain: Retrieve and update durable personal or project context
policy-monitor: Gizlilik politikası, aydınlatma metinleri, açık rıza metinleri, çerez/CMP
sepia: asked to humanize, de-AI, unslop, or strip AI
sms: wants to plan, build, or optimize SMS, MMS
stop-slop: drafting, editing, or reviewing text to eliminate predictable
<!-- dizin:son -->
