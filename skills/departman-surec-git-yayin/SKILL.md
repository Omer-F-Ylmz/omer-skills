---
name: departman-surec-git-yayin
description: "Git ve yayın müdürü: commit, PR, CI, deploy, canary ve kapanış sırası. Commit, push, ship ya da deploy adımında oku."
---

# Departman: surec-git-yayin — iş sırası

Katalog: `docs/departmanlar/surec-git-yayin.md` · yaşam döngüsü `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

## Adımlar
1. **Dal** — yalıtım gerekirse `using-git-worktrees`; akış kuralları `git-workflow-and-versioning`.
2. **Commit** — `commit-commands` (kırmızı ve yeşil ayrı commit); push öncesi `departman-guvenlik` adım 1.
3. **CI** — `ci-cd-and-automation`; kırmızı CI'da yayın yok.
4. **Yayın** — `ship` / `land-and-deploy`; Vercel `deploy-to-vercel`; yayın sonrası `canary`.
5. **Kapanış** — `finishing-a-development-branch`; rapor ≤15 satır (commit · test · CI · sapma), omer-kurallar:15.

## Kapılar
- Kullanıcı istemeden push/deploy yok; default dalda önce dal aç.
- Sır taraması temiz olmadan push yok.
- Paralel ajan kolunda her commit `git commit --trailer "Gorev: <AD>"` taşır; birleştirmede "zaten var/özdeş" iddiası `git cherry -v main <kol>` ile (patch-id; `-` = içerikçe main'de) kanıtlanır, rapora commit → görev satırı (KAYNAK-5, Atlas).

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- hetzner-deploy (1): hetzner-deploy · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->


Slash katalog (iş türü → /komut·skill): `yetenek-getir/reference/slash-katalog.md` — Read; oturuma yüklenmez.

<!-- dizin:bas -->
## Dizin: adımdaki araç işe uymuyorsa `references/dizin.md` dosyasını oku, listeden adla çağır.
<!-- dizin:son -->
