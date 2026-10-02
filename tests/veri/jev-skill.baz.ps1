# UserPromptSubmit: Jev skill ipucu (KURULUM-13c). Fail-open: her durumda exit 0.
# Kapı, günlük tavan, redaksiyon ve 2 sn bütçe Python'da (tools/jev/jev/skill.py hook); burası yalnız sarmalayıcı.
$ErrorActionPreference = 'SilentlyContinue'
try {
  $kapi = [Environment]::GetEnvironmentVariable('JEV_SKILL_HOOK', 'User')
  if ($kapi -ne '1') { exit 0 }
  $env:JEV_SKILL_HOOK = $kapi
  $girdi = [Console]::In.ReadToEnd()
  $psi = New-Object Diagnostics.ProcessStartInfo 'python', '-m jev hook'
  $psi.WorkingDirectory = 'C:\Projeler\omer-skills\tools\jev'
  $psi.RedirectStandardInput = $true; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
  $psi.UseShellExecute = $false; $psi.CreateNoWindow = $true
  $psi.StandardOutputEncoding = [Text.Encoding]::UTF8
  $p = [Diagnostics.Process]::Start($psi)
  $yaz = New-Object IO.StreamWriter($p.StandardInput.BaseStream, (New-Object Text.UTF8Encoding $false))
  $yaz.Write($girdi); $yaz.Close()
  $oku = $p.StandardOutput.ReadToEndAsync()
  if (-not $p.WaitForExit(2500)) { $p.Kill(); exit 0 }
  $cikti = $oku.Result
  if ($cikti) {
    $bytes = (New-Object Text.UTF8Encoding $false).GetBytes($cikti.Trim())
    $out = [Console]::OpenStandardOutput(); $out.Write($bytes, 0, $bytes.Length); $out.Flush()
  }
} catch { }
exit 0
