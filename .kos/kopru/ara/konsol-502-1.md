# KONSOL-502-1 ara not (25 Eki 01:00)
- 6767 = headroom-desktop.exe (pid 21012, --autostart) proxy; settings.json'da 6767 kaydı Eylül'den beri yedeklerde var, yeni katman değil.
- 502 kök neden: proxy değil, sistem UDP/DNS. headroom log: "Failed to connect to upstream API: [Errno 11001] getaddrinfo failed" (00:04'ten beri).
- Kanıt: socket.getaddrinfo example.com da düşüyor; TCP 1.1.1.1:443 açık; Resolve-DnsName -Server 1.1.1.1 → WSAENOBUFS. Get-NetUDPEndpoint: 16409 toplam, MSI.CentralServer (pid 9308) tek başına 16376 (UDP soket sızıntısı).
- Düzeltme (MSI.CentralServer'ı durdur) sınıflandırıcı tarafından reddedildi → Ömer onayı bekliyor.
- Yapılmadı: işlerin yeniden koşusu (DNS düzelmeden 502 tekrarlar), global ayara geri ekleme, claude -p 200 kanıtı.
- Konsol bayrağı: ajan-sira.konsol dosyası 20:30 tarihli, şu an açık; kimin kapattığı ajan-sira.log'da yok (kapatma = yeniden adlandırma, iz bırakmıyor).
