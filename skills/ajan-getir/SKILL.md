---
name: ajan-getir
description: Use when a task fits a specialist agent that is not in the Agent tool's list (284 installed agents: hidden + visible plugin agents and user agents, e.g. "Database Optimizer", "octo:droids:octo-debugger"), or when the user says /ajan-getir AD-or-topic. Finds the agent in katalog.tsv and runs it as a general-purpose subagent with that agent's prompt and model.
---

# ajan-getir

Gizli ajanlar (settings.json `Agent(...)` deny listesi) ve kullanıcı ajanları Agent aracında görünmez; deny listesi DEĞİŞMEZ. Bu skill onları general-purpose alt ajanla taklit eder.

1. **Bul:** `katalog.tsv` (bu klasörde; sütunlar ad · model · tek_satir · yol) Grep ile ara — konu kelimesi veya ad. Katalogu baştan sona okuma. Ajan Agent aracında zaten görünüyorsa doğrudan onu çağır. Birden çok aday → tek satırına göre en uygununu seç; belirsizse kullanıcıya 2–3 aday göster.
2. **Oku:** seçilen satırın `yol` dosyasını Read ile oku (claude.ai paketinde yol bu skill klasörüne göreli: `references/ajanlar/…`); frontmatter sonrası gövde = ajanın sistem istemi.
3. **Koş:** Agent aracı, `subagent_type: general-purpose`, `model`: katalogdaki model (`sonnet`/`opus`/`haiku`; `inherit` → model verme). Prompt:
   ```
   Aşağıdaki rolü üstlen ve görevi yap.
   <rol>{gövde}</rol>
   <gorev>{kullanıcının işi + gerekli dosya yolları}</gorev>
   Çıktıyı {çıktı yolu} dosyasına yaz; bana yalnız yol + ≤5 satır özet dön.
   ```
   Agent aracı yoksa (claude.ai): rolü bu konuşmada üstlen, görevi kendin yap.
4. **Doğrula:** çıktı dosyasının var olduğunu kontrol et; yolu kullanıcıya ver.

Katalog eskidiyse (yeni plugin/ajan): `python tools/ajan_katalog.py` (omer-skills reposunda) yeniden üretir.
