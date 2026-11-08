import subprocess, glob, os, time, json
o = subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -notlike '*WindowsApps*' -and ($_.Name -eq 'blender.exe' -or $_.CommandLine -like '*cc-kopru*' -or $_.CommandLine -like '*claude*--output-format*') } | ForEach-Object { '{0} {1} {2}MB {3} {4}' -f $_.ProcessId,$_.Name,[int]($_.WorkingSetSize/1MB),$_.CreationDate.ToString('HH:mm'),$_.CommandLine.Substring(0,[Math]::Min(140,$_.CommandLine.Length)) }"], capture_output=True, text=True, timeout=60)
print(o.stdout, o.stderr[:300])
fs = sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime)[-4:]
for f in fs:
    print('==', time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(f))), f[-60:])
    ls = open(f, encoding='utf-8', errors='replace').read().splitlines()[-3:]
    for l in ls:
        try:
            d = json.loads(l); m = d.get('message', {}); c = m.get('content')
            if isinstance(c, list):
                for x in c:
                    t = x.get('type'); s = x.get('text') or json.dumps(x.get('input') or x.get('content'), ensure_ascii=False)
                    print('  ', d.get('type'), t, str(s)[:200].replace('\n', ' '))
            else:
                print('  ', d.get('type'), str(c)[:200].replace('\n', ' '))
        except Exception as e:
            print('  ?', l[:120])
