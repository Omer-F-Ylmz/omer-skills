# ret-kur-1-a, güvenlik adımı (eksik tur)
skillspector scan --no-llm (degraded, kesin temiz sayılmaz); rapor: .kos/kopru/ara/ss/*.json. Graft: 170 sn zaman aşımı (taranamadı; gitleaks 21 = test fixture).
repo | high | med | low | ana kategori
design-skills | 2 | 11 | 0 | Prompt Injection
system-one-connector | 10 | 19 | 3 | Rogue Agent/Priv.Esc.
JEV_Claude_plugin (klukacin) | 93 | 91 | 7 | Tool Misuse/Agent Snooping
typesafe-mcp | 19 | 26 | 0 | Agent Snooping
jev-mcp (rashedInt32) | 24 | 7 | 8 | Priv.Esc./Supply Chain
jev-reach | 6 | 2 | 8 | Supply Chain
morning-briefer | 12 | 2 | 0 | Priv.Esc.
Karar: hiçbiri CC'de etkin değil (settings/known_marketplaces'te yok; yalnız onay/ret_kur_1_uygula.py marketplace ekler). Onay betiği çalıştırılmadan önce high bulgular (özellikle klukacin) elle gözden geçirilmeli.
security-reviewer skill'i skillOverrides ile model çağrısına kapalı: SKILL.md Read ile okundu (8 maddelik kontrol; kod değişikliği yok, uygulanacak diff yok).
