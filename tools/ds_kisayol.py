import subprocess
from pathlib import Path

kok = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored")
ps1 = kok / "baslat.ps1"
cmd = Path.home() / ".local" / "bin" / "claude-ds.cmd"
icerik = '@echo off\r\npowershell -NoProfile -ExecutionPolicy Bypass -File "%s" %%*\r\n' % ps1
cmd.write_bytes(icerik.encode("ascii", "replace") if False else icerik.encode("utf-8"))
anahtar = r"HKCU\Software\Classes\Directory\Background\shell\ClaudeDeepSeek"
komut = 'wt.exe -d "%%V" cmd /k "%s"' % cmd
s = []
for k in ([anahtar, "/ve", "/d", "DeepSeek ile Claude Code"],
          [anahtar, "/v", "Icon", "/d", r"C:\Users\pc\.local\bin\claude.exe"],
          [anahtar + r"\command", "/ve", "/d", komut]):
    r = subprocess.run(["reg", "add"] + k + ["/f"], capture_output=True, text=True, errors="replace")
    s.append("%s %s" % (r.returncode, (r.stdout + r.stderr).strip()))
r = subprocess.run(["where", "wt.exe"], capture_output=True, text=True)
s.append("wt: " + r.stdout.strip())
s.append("cmd: %s %s" % (cmd, cmd.exists()))
(kok / "kisayol.txt").write_text("\n".join(s), encoding="utf-8")
