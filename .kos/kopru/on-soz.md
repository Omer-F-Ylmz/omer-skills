ÖN SÖZ (ARAÇ-DENETİM-1; her görevde, görev dosyasında tekrar yazılmaz)
1. İş türünü tek kelimeyle sınıfla (site-3d · video · güvenlik · belge · logo · render · diğer). Eşleşen atlas kitabını aç: docs/atlas/<kitap>.md (site-3d, video-icerik, guvenlik-test, belge-sunum); varsa departman-* müdür skill'ini izle.
2. Eksik araç için `python tools/katalog_ara.py "<iş tarifi>"` en fazla 3 sorgu. Hazır çözüm (skill tarifi, bileşen, CC0 varlık) varsa önce onu al, sonra özgünleştir.
3. Alt görevlere tür ata: `python tools/yonlendir.py sec <tür>`; dönen kararı uygula.
4. Görseli tam boyda okuma: önce küçült/kırp, sonra oku.
5. Rapor sonuna tek satır: `araç: <skill/MCP/CLI — adım>` + `$` + model dağılımı.
