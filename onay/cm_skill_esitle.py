"""code-mode SKILL.md: repo -> ~/.claude/skills/code-mode (CC) + claude.ai zip'i yeniden uret."""
import os, shutil, zipfile
REPO = r"C:\Projeler\omer-skills\skills\code-mode"
CC = os.path.expanduser(r"~\.claude\skills\code-mode")
ZIP = r"C:\Projeler\omer-skills\dist\claude-ai\yukle-23eki\code-mode.zip"
os.makedirs(CC, exist_ok=True)
for f in os.listdir(REPO):
    shutil.copy2(os.path.join(REPO, f), os.path.join(CC, f))
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(REPO):
        z.write(os.path.join(REPO, f), "code-mode/" + f)
print("CC:", sorted(os.listdir(CC)), "| zip:", zipfile.ZipFile(ZIP).namelist(), os.path.getsize(ZIP))
