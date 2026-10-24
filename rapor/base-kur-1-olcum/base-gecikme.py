import subprocess,time,json,statistics,os
cwd=r'C:\Projeler\omer-skills'
pl={
 'session-start':{'hook_event_name':'SessionStart','session_id':'olcum-1','cwd':cwd,'source':'startup'},
 'user-prompt-submit':{'hook_event_name':'UserPromptSubmit','session_id':'olcum-1','cwd':cwd,'prompt':'bu fonksiyonun kullanim yerlerini bul'},
 'pre-tool-use':{'hook_event_name':'PreToolUse','session_id':'olcum-1','cwd':cwd,'tool_name':'Read','tool_input':{'file_path':cwd+r'\README.md'}},
 'post-tool-use':{'hook_event_name':'PostToolUse','session_id':'olcum-1','cwd':cwd,'tool_name':'Read','tool_input':{'file_path':cwd+r'\README.md'},'tool_response':{'content':'x'}},
 'stop':{'hook_event_name':'Stop','session_id':'olcum-1','cwd':cwd,'stop_hook_active':False},
 'session-end':{'hook_event_name':'SessionEnd','session_id':'olcum-1','cwd':cwd,'reason':'other'},
}
for h,p in pl.items():
    ts=[];n=0
    for i in range(5):
        t=time.perf_counter()
        r=subprocess.run(['base','hook',h],input=json.dumps(p),capture_output=True,text=True,cwd=cwd,creationflags=0x08000000)
        ts.append(time.perf_counter()-t); n=len(r.stdout)
    print(f'{h}: med {statistics.median(ts):.2f}s max {max(ts):.2f}s rc={r.returncode} out={n}B')
