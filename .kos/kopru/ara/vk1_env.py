import os,json,subprocess,pathlib,re
H=pathlib.Path.home();inv=set()
def add(s):
    for t in re.split(r'[^a-z0-9]+',s.lower()):
        pass
    inv.add(s.lower())
for p in (H/'.claude/skills').iterdir(): add(p.name)
for p in pathlib.Path('.claude/skills').glob('*') if pathlib.Path('.claude/skills').exists() else []: add(p.name)
try:
    d=json.load(open(H/'.claude/settings.json',encoding='utf-8'))
    for k in d.get('enabledPlugins',{}): add(k.split('@')[0]); add(k)
except Exception as e: print('set',e)
try:
    d=json.load(open(H/'.claude/plugins/installed_plugins.json',encoding='utf-8'))
    for k in d.get('plugins',d): add(k.split('@')[0])
except Exception as e: print('ip',e)
for f in (H/'.claude.json',pathlib.Path('.mcp.json')):
    try:
        d=json.load(open(f,encoding='utf-8'))
        for k in d.get('mcpServers',{}): add('mcp:'+k)
        for pr in d.get('projects',{}).values():
            for k in pr.get('mcpServers',{}): add('mcp:'+k)
    except Exception as e: pass
def run(c):
    try: return subprocess.run(c,capture_output=True,text=True,shell=True,timeout=90,encoding='utf-8',errors='replace').stdout
    except Exception: return ''
for l in run('npm ls -g --depth=0').splitlines()[1:]:
    m=re.search(r'[├└]── (\S+)@',l)
    if m: add('npm:'+m.group(1).lower())
for l in run('pip list --format=freeze').splitlines(): add('pip:'+l.split('==')[0].lower())
for l in run('uv tool list').splitlines():
    if l and not l.startswith('-'): add('uv:'+l.split()[0].lower())
for l in run('powershell -NoProfile -Command "(Get-StartApps|%{$_.Name}) -join [char]10"').splitlines(): add('app:'+l.strip().lower())
for l in run('winget list --accept-source-agreements').splitlines()[3:]: add('app:'+l[:40].strip().lower())
for l in run('gh extension list').splitlines(): add('gh-ext:'+l.split()[-1].lower() if l.split() else '')
for b in ['ffmpeg','yt-dlp','gitleaks','semgrep','strix','blender','ollama','gh','rtk','headroom','playwright','whisper','node','uv','docker','bun','deno']:
    if run(f'where {b}').strip(): add('bin:'+b)
open('.kos/kopru/ara/vk1_env.txt','w',encoding='utf-8').write('\n'.join(sorted(inv)))
print(len(inv))
