import os, hashlib
a = os.path.expanduser(r"~\.claude\skills\code-mode\SKILL.md")
b = r"C:\Projeler\omer-skills\skills\code-mode\SKILL.md"
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:12] if os.path.exists(p) else "YOK"
print("CC global:", h(a), "| repo:", h(b), "| ayni:", h(a) == h(b))
