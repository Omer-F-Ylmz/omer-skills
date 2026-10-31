import json,io,os,sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'tools')
D='.kos/kopru/mem-abone/'
src=open(D+'deney.py',encoding='utf8').read()
exec(src.split("def kaynak")[0])
exec("JP="+src.split("JP=")[1].split("def isle")[0])
SK="""
SKIP CRITERION: Reply <skip_summary reason="..." /> ONLY for pure routine noise (directory listing, status check, re-reading a file, a command with no result that changes understanding). If the event shows a change made, a bug/error found, a decision, a measured result, or a new fact about the project, write the observation instead.
"""
SJ="""You are judging whether a coding-session event deserves a durable memory observation. DURABLE = a change made, an error/bug found, a decision, a measured result, or a new project fact. NOISE = routine listing, status check, re-read with nothing new. Reply ONE word: DURABLE or NOISE, then at most 10 words of reason.
EVENT:
%s"""
R=[json.loads(l) for l in io.open(D+'deney5.jsonl',encoding='utf-8')]
def isle(r):
    u=r['src'];o={'src':u[:200]}
    o['sj']=haiku(SJ%u[:3000])                  # kör: modelin kararını görmez
    o['C']=haiku(TABAN+SK+"\n\n"+u+"\nProduce the observation XML now.")
    if not o['C'].lstrip().startswith('<skip_summary'): o['j1C']=haiku(JP%(u,o['C']))
    o['A']=r['A'];o['B']=r['B'];o['live']=r['live']
    io.open(D+'deney6.jsonl','a',encoding='utf-8').write(json.dumps(o,ensure_ascii=False)+'\n');return o
with ThreadPoolExecutor(3) as ex: res=list(ex.map(isle,R))
print(len(res))
