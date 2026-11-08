import re
from pathlib import Path

kok = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored")
t = (kok / "sunucu.log").read_text(encoding="utf-8", errors="replace").splitlines()
s = [l for l in t if re.search(r"prompt eval time|eval time|n_ctx|offloaded|CUDA0 model buffer|CPU_Mapped|slot update|n_tokens|error|failed", l)]
(kok / "ds_log.txt").write_text("\n".join(s[-40:]), encoding="utf-8")
