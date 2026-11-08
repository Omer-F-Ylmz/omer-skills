import subprocess

r = subprocess.run(
    ["uv", "tool", "install", "leann", "--python", "3.12", "--force", "-v"],
    capture_output=True, text=True, timeout=480,
)
satirlar = (r.stdout + r.stderr).splitlines()
for i, l in enumerate(satirlar):
    if "entrypoint" in l.lower() or "error" in l.lower():
        print("\n".join(satirlar[max(0, i - 6): i + 8]))
        print("----")
print("TOPLAM SATIR", len(satirlar))
print("\n".join(satirlar[-12:]))
print("exit", r.returncode)

r = subprocess.run(["uv", "--version"], capture_output=True, text=True)
print(r.stdout)
