# ÖĞREN-6 G4 test-qa — kapanış (20 Eki)

Kapsam: dotnet-test skill'leri · tdd · playwright-cli/MCP · webapp-testing · gstack-qa · verification-loop · eval-harness · jev · grade-tests · run-tests (G4: test-qa + güvenlik + backend-dotnet + veri-db, kart dizini `.kos/kopru/ogren/kart.jsonl`).

## Kapı
İki yeni tohum, tohum başı iki kör hakem (100 alan: ne_yapar · komut · sınırlar · mekanizma):
- t67: a %95 · b %96
- t68: a %94 · b %93
Kalan Y'ler: careful (komut), playwright-cli · check-bin-obj-clash (sınırlar), tm-security-review (mekanizma); phoenix-security-review · opengrep-rule-generator(-research) · crap-score (sınırlar), crap-score · qa (komut), qa (ne_yapar). Hakem kayıtları: `.claude/ogren6/h67{a,b}.jsonl`, `h68{a,b}.jsonl`.
Uyarı: t67-b hakemi büyük kaynakları (semgrep, writing-mstest-tests, convert-blazor-server-to-webapp) tam okumadığını bildirdi; t68-b tam okudu.

## Yöntem dersi
Komut ve sınır alanları kaynaktan betikle (`duzelt.py`/`duzelt2.py`) doldurulur; "belirsiz" yalnız kaynakta gerçekten yoksa. Müdür skill: `skills/departman-test-qa/SKILL.md` (adım 3 kapsam biçimi, adım 5 pixeljury = LLM yargıç, Ders satırı).

## Borç (`.kos/kopru/ogren/ogren-6-borc.tsv`, olduğu gibi)
dotnet · veri-db · çapraz kombin yok; jev metin puanlama ve Desktop kombin denenmedi; 6 gstack kartı komutu `gstack-skill-start`; 5 kartta açıklama alıntısı >700 krk; `.claude/ogren6/tmp65b/` geçici dosya silinmedi.
