# YÖNETİCİ-BAĞIMSIZ-1 d2: "AjanSira" görevi — oturum açınca + 10 dk'da bir bekçi turu (yönetici canlıysa yenisi hemen çıkar; ölmüşse devralır), elle: schtasks /Run /TN AjanSira
$ErrorActionPreference = 'Stop'
$kok = 'C:\Projeler\omer-skills'
$pyw = (Get-Command pythonw.exe).Source
$a = New-ScheduledTaskAction -Execute $pyw -Argument ('"{0}\.kos\kopru\yonetici_gorev.py"' -f $kok) -WorkingDirectory $kok
$t = @((New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME),
       (New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Days 3650)))
$s = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -Hidden
$p = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'AjanSira' -Action $a -Trigger $t -Settings $s -Principal $p -Force | Out-Null
(Get-ScheduledTask -TaskName 'AjanSira').State
