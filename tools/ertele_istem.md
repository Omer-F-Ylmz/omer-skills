# Skill/ajan ertelenmiş yükleme
Bu oturumda skill ve özel ajan listesi bağlama yüklenmedi (Skill aracı kapalı; ajan listesi kısaltıldı). Hiçbiri silinmedi: hepsi katalogda.
İş bir skill/ajan gerektirebiliyorsa ÖNCE ara, sonra tam metni yükle:
1. `python C:/Projeler/omer-skills/tools/ertele_katalog.py ara "<iş özeti>"` → aday adlar (ad · tür · tek satır)
2. `python C:/Projeler/omer-skills/tools/ertele_katalog.py tam <ad>` → skill/ajan tanımının tam metni; talimatı bu metne göre uygula.
3. Yüklediğin `departman-*` yönetici skill'i yalnız sırayı verir; işi yapan değildir. Yönetici metninin bu iş için adını verdiği İLGİLİ ÖZEL skill'in (departman-* olmayan, işin asıl uygulayıcısı) tam metnini de `tam <ad>` ile MUTLAKA yükle; ad bulunamazsa `ara` ile özel skill'i bul. Planı özel skill'in adım/komutlarına dayandır, yöneticiyi yalnız sıra için kullan.
4. İstemde kancanın verdiği bir `<katalog>` bloğu varsa `ara` çağırma; oradaki uygun adları doğrudan `tam <ad>` ile yükle (katalogdaki "Skill <ad>" çağrısı bu oturumda kapalı, yerine `tam` kullan). Katalogda uygun ad yoksa `ara` kullan.
Ajan türü ise: tanım metnini Agent(subagent_type="general-purpose") istemine koyarak çalıştır.
