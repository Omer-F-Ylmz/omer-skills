' Windows oturum açılışında gizli pencerede WSL'i ayakta tutar ve docker'ı başlatır (Postiz konteynerleri restart: always).
CreateObject("WScript.Shell").Run "wsl.exe -d Ubuntu -u root -e bash -c ""systemctl start docker; cd /opt/postiz && docker compose up -d; sleep infinity""", 0, False
