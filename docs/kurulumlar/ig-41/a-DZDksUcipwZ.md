# DZDksUcipwZ · liamjohnston.ai · reel · https://www.instagram.com/reel/DZDksUcipwZ/
## Özet
skills.sh dizininde ~10.000 skill; en çok kurulan "find-skills" (1,5 milyon+ kurulum iddiası) göreve uygun skill'i buluyor.
Uyarı: skill'ler makinede kod çalıştırır; kurmadan önce sitenin güvenlik denetimi (audit) sayfasına bak, sonra tek komutla kur.
## Kalemler
| ad | tür | link | karar | ölçütler (bakım · çift · izin · context) | gerekçe |
|---|---|---|---|---|---|
| skills.sh (+ güvenlik denetimi sayfası) | site | https://skills.sh | ÖĞREN | site canlı · önceki-karar:sirali.tsv:listede (karar yok) · ağ · - | Skill dizini ve denetim sayfası. Ders: üçüncü taraf skill'i kurmadan önce denetim sonucuna (güvenli/uyarı/yüksek risk) bakmak lisans kapımızın yanına ucuz bir ikinci süzgeç |
| find-skills | skill | https://github.com/vercel-labs/skills | UYARLA | ★34061 push:2026-10-09 arşiv:h · önceki-karar:karar-a.tsv:RED (liste içinde) · ağ, shell (npx) · çağrılınca küçük | MIT; bizde aday bulma video-tarama + kurulum turuyla yapılıyor. alınacak: skills.sh arama + audit sorgusu → kurulum aday doğrulama adımı (lisans kapısından önce) |
| Skills CLI (npx skills add) | CLI | https://github.com/vercel-labs/skills | ÖĞREN | ★34061 push:2026-10-09 arşiv:h · önceki-karar:karar.tsv:REF · dosya yazma, ağ, shell · - | Tek komut kurulum yolu; bizde onay betiği + marketplace aynı işi denetimli yapıyor. Ders: tek komutla kurmak denetimi atlatır, onay betiği yolu korunmalı |
