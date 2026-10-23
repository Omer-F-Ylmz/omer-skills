# YONETICI-OLUM-2 ara not (23 Eki 18:31)
- Görev XML temiz: ExecutionTimeLimit PT0S, StopIfGoingOnBatteries False, RunOnlyIfIdle False, IgnoreNew, StartWhenAvailable. LastTaskResult 0x800710E0 = IgnoreNew (10 dk tiki, yönetici canlı), normal.
- Başlama saatleri tam 40 dk arayla: 15:31:31, 16:11:01, 16:51:02, 17:31:00, 18:11:02 → bir şey ~40 dk'da öldürüyor; ölen yönetici günlüğe istisna yazmıyor (stderr günlüğe bağlı) → Python istisnası değil, dıştan sonlandırma/oturum kesilmesi.
- Kanıt düzeneği: .kos/kopru/yonetici_kalp.py (30 sn kalp: yonetici-kalp.txt; atexit; excepthook; faulthandler → yonetici-fault.txt; yeni yönetici önceki ölümü yonetici-olum.log + ajan-sira.log "ÖNCEKİ ÖLÜM" satırına yazar).
- Devam: yeni kodu ilk 40 dk'lık ölümden sonraki başlatma yükler; sonra `type .kos\kopru\yonetici-olum.log` ve ajan-sira.log "ÖNCEKİ ÖLÜM" bak. "çıkış izi yok" + boot aynı = TerminateProcess/oturum; "yeniden başlatma" = makine.
