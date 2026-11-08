import sys
sys.path.insert(0, r"C:\Projeler\omer-skills\tools")
from PIL import Image
import sunucu_rig as R
bg = {"robot": (14, 12, 48, 255), "owl": (7, 11, 36, 255)}
sheet = Image.new("RGBA", (1000 * 3 // 2, 1000 * 4 // 2), (0, 0, 0, 255))
i = 0
for ch in ("robot", "owl"):
    for kw in (dict(), dict(yaw=0.5, expr="curious"), dict(yaw=1.0), dict(expr="laugh"), dict(expr="eureka", armR=175), dict(expr="suspicion")):
        t = Image.new("RGBA", (1000, 1000), bg[ch]); t.alpha_composite(R.CHARS[ch](**kw)); t = t.resize((500, 500))
        sheet.paste(t, ((i % 3) * 500, (i // 3) * 500)); i += 1
sheet.convert("RGB").save(sys.argv[1])
