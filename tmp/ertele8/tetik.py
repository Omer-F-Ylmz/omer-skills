"""ERTELE-3 TUR4 madde 5: her komut yeniden yükleme bloğunun başından önceki 4 satır (tetikleyici)."""
import re, sys
sat = open(sys.argv[1], encoding="utf-8", errors="ignore").read().splitlines()
yuk = re.compile(r"Loaded \d+ commands from plugin|Checking commandPath|Failed to parse YAML|\[skills\] YAML|No commands found in plugin")
blok = False
for i, s in enumerate(sat):
    if yuk.search(s):
        if not blok:
            print(f"--- blok @{i}")
            for o in sat[max(0, i - 4):i]:
                print("   ", o[:200])
        blok = True
    elif blok and i + 1 < len(sat) and not yuk.search(sat[i + 1]):
        blok = False
