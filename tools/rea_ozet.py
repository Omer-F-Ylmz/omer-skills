"""REA sonucunu (tool-results/mcp-rea-*.txt) kisa teknik ozete indirger; hedef -> docs/site-inceleme/rea/<site>.json. Kullanim: rea_ozet.py <site-adi> [dosya] (dosya yoksa en yeni)."""
import glob, json, os, re, sys
from collections import Counter
D = r"C:\Users\pc\.claude\projects\C--Projeler-omer-skills\2abaad37-150d-439c-af95-e02d065e7642\tool-results"
fs = [sys.argv[1]] if len(sys.argv) > 1 else sorted(glob.glob(D + r"\mcp-rea-inspect_web_page-*.txt"))
for f in fs:
  try:
    n = json.load(open(f, encoding="utf-8"))["normalized_result"]
  except Exception:
    continue
  ad = re.sub(r"^www\.", "", n["target"]["url"].split("/")[2])
  if os.path.exists("docs/site-inceleme/rea/%s.json" % ad):
    continue
  sc = [s.get("url") or s.get("src") or "" for s in n["scripts"]["items"]]
  dosya = [os.path.basename(u.split("?")[0]) for u in sc if u]
  txt = json.dumps(n["scripts"]["items"]) + json.dumps(n["resources"])[:20000]
  VEND = {k: bool(re.search(p, txt, re.I)) for k, p in dict(three="three(\.module|\.min)?\.js|/three", gsap="gsap", lenis="lenis", framer="framer-motion|framerusercontent", react="react", next="/_next/", vue="vue", webflow="webflow", tailwind="tailwind", spline="spline", rive="rive", lottie="lottie", barba="barba", swiper="swiper").items()}
  tag = Counter(x.get("tag") or x.get("name") for x in n["dom"]["nodes"][:3000] if isinstance(x, dict))
  o = dict(site=ad, url=n["target"]["url"], title=n["target"]["title"][:80], dom=n["dom"]["total_nodes"], scripts=n["scripts"]["total"],
           vendor=[k for k, v in VEND.items() if v], canvas=tag.get("canvas", 0), req=len(n["network"]["requests"]) if isinstance(n["network"]["requests"], list) else n["network"]["requests"],
           ana_dosya=dosya[:8])
  os.makedirs("docs/site-inceleme/rea", exist_ok=True)
  json.dump(o, open("docs/site-inceleme/rea/%s.json" % ad, "w", encoding="utf-8"), ensure_ascii=False)
  print(json.dumps(o, ensure_ascii=False))
