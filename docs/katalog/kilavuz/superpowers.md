# superpowers — 4 benzersiz kayıt

**Amaç:** Superpowers iş akışı skill'lerinin tekil kopyaları: planı uygulama, alt ajan güdümlü geliştirme, skill yazma; ayrıca Çince sürüm paketi.

**İç yapı:** Ad kalıbı superpowers-<konu>: superpowers-executing-plans, superpowers-subagent-driven-development, superpowers-writing-skills ve superpowers-zh-paket (Çince).

## En güçlü parçalar
- `superpowers-executing-plans` — Uygulama planını mevcut oturumda bizzat uygulayıcı olarak yürütür.
- `superpowers-subagent-driven-development` — Bağımsız görevli planları mevcut oturumda alt ajanlarla yürütür.
- `superpowers-writing-skills` — Skill oluşturma, düzenleme ve yayın öncesi çalıştığını doğrulama.

## Birlikte kullanım
- superpowers-executing-plans ya da superpowers-subagent-driven-development: planın bağımsız görevlerine göre biri seçilir.
- superpowers-writing-skills + skill ailesindeki skill-scanner: yazılan skill'i taramak.
- claude-plugins-official'daki superpowers:writing-plans ile plan üretip burada uygulamak.

## Tuzaklar
- superpowers-writing-skills, writing ailesindeki writing-skills ile aynı açıklamaya sahip; çift kopya.
- superpowers-zh-paket Çince sürümdür; Türkçe/İngilizce işte gereksiz.

## Üyeler
- skill (4): superpowers-executing-plans, superpowers-subagent-driven-development, superpowers-writing-skills, superpowers-zh-paket
