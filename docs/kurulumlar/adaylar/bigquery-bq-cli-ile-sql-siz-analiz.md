# BigQuery bq CLI ile SQL'siz analiz
ad: BigQuery bq CLI ile SQL'siz analiz
tur: CLI
video: jqoFP9QapXI
repo: yok
lisans: Apache-2.0
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bq CLI, Google Cloud SDK'nın kullanım istatistiği ayarına tabidir (`gcloud config set disable_usage_reporting true` ile kapatılır). Sorgular Google'a gider. Claude Code tarafında sorgu sonuçları Anthropic API'ye bağlam olarak gönderilir. Kesin ayrıntı doğrulanmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Google Cloud SDK ile gelen `bq` komut satırı aracını Claude Code'a bağlayıp BigQuery verisini doğal dille sorgulatma yöntemi. Kullanıcı soruyu Türkçe/İngilizce sorar, Claude SQL'i üretir ve `bq query` ile çalıştırır.
## Mekanizma
Claude Code'un Bash aracı yüklü `bq` CLI'sini çağırır: önce `bq ls` / `bq show --schema` ile şemayı keşfeder, sonra doğal dil isteğinden SQL üretip `bq query --use_legacy_sql=false` ile çalıştırır, çıktıyı (CSV/JSON) okuyup yorumlar. Kimlik doğrulama gcloud (`gcloud auth login`) üzerinden yapılır. Ayrı bir eklenti gerekmez; video yalnızca "BQ gibi CLI araçlarını Claude Code'a bağla" diyor. Video sayfası metni alınamadı, ayrıntılar doğrulanamadı.
## Kanıt
- Claude Code bq CLI'sine bağlanıp doğal dilden SQL üretip çalıştırabilir → sınanamadı · Video sayfası metni (video getir) yalnızca başlık '32 Tricks to Level Up Claude Code in 16 Mins' ve YouTube altbilgisi döndürdü; transkript yok. Mekanizma Bash aracı ve bq'nun genel bilgisiyle makul ama denenmedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Google Cloud SDK'yı kur (https://cloud.google.com/sdk/docs/install); `bq` içinde gelir
- `gcloud auth login` ve `gcloud config set project <PROJE_ID>`
- Test: `bq ls` ve `bq query --use_legacy_sql=false 'SELECT 1'`
- Claude Code'a veri setini ve salt-okunur kural talimatını CLAUDE.md'de ver
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
SQL bilmeden doğal dille veri analizi yapılır. Ek eklenti ya da MCP gerekmez, kurulum küçüktür.
## Maliyet/risk
Claude yanlış ya da pahalı SQL üretebilir; BigQuery taranan bayta göre faturalandırır. Yazma, silme ve DDL riski var. Sonuçlardaki hassas veri modele gider. Azaltma: salt-okunur IAM rolü, `--dry_run`, `--maximum_bytes_billed` ve izin listesi kullan. Kanıt yalnızca video başlığı; içerik doğrulanamadı.
## Tasarruf
Token aracı değil. Dolaylı olarak, büyük veriyi bağlama yüklemek yerine sorguyu BigQuery'de çalıştırıp yalnızca özet sonucu döndürmek bağlamı küçük tutar.
## Üretilebilir
hedef_tur: skill
tarif: `bigquery-analiz` skill'i yaz. Adımlar: (1) `bq ls` ve `bq show --schema --format=prettyjson` ile şemayı keşfet; (2) SQL üret; (3) her zaman önce `bq query --dry_run` ile bayt tahmini al, eşiği aşarsa kullanıcıya sor; (4) `--maximum_bytes_billed` ve `LIMIT` ile çalıştır; (5) yalnızca SELECT'e izin ver, DDL/DML'i reddet; (6) sonucu tablo ve özet olarak sun. Hook ile `bq` komutlarında INSERT/DELETE/DROP'u engelle.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### `bq query` ile standart SQL çalıştırma, `--dry_run` ile maliyet tahmini, `--maximum_bytes_billed` ile tarama sınırı
kaynak: https://cloud.google.com/bigquery/docs/bq-command-line-tool
## Destek
- jqoFP9QapXI · 12:30 · Doğal dille sorgu, Claude SQL üretip çalıştırır. · kanıt: connect CLI tools like BigQuery's BQ tool to Claude code
