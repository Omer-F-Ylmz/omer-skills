' Windows oturum açılışında gizli pencerede WSL'i ayakta tutar ve docker'ı başlatır (Postiz konteynerleri restart: always).
CreateObject("WScript.Shell").Run "wsl.exe -d Ubuntu -u root -e bash -c ""systemctl start docker; sleep infinity""", 0, False
