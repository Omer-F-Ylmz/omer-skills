# TokenEconomizer refresh-catalog, 60 sn sabit zaman asimi yerine uzun sure (claude -p acilisi bu makinede ~340 sn)
import sys, time, functools
sys.path.insert(0, r"C:/AI/indirilen/video-izle-kur-1/TokenEconomizer/plugin/lib")
from tokeneconomizer.plugin import toolcheck, cli
toolcheck._init_tools = functools.partial(toolcheck._init_tools, timeout=int(sys.argv[1]) if len(sys.argv) > 1 else 600)
t = time.time()
path, tools = toolcheck.refresh_catalog(cli.state_root(), host="claude")
print("sure", round(time.time() - t), "arac", len(tools), path)
