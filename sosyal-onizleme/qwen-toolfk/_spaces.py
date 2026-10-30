import sys
from playwright.sync_api import sync_playwright
slugs="online-img-to-vide* online-text-to-vide* hf-wan-image-to-video ai-image-upscaler online-removerized ai-object-remover ai-remove-people-from-photos online-ocr hf-paddleocr ai-tts ai-youtube-thumbnai* ai-2d-to-3d-image-* ai-background-remover".split()
import re
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(); pg.set_default_timeout(20000)
    pg.goto("https://www.toolfk.com/",wait_until="commit",timeout=40000); pg.wait_for_timeout(4000)
    hrefs=pg.eval_on_selector_all("a","e=>e.map(x=>x.href)")
    hrefs=sorted({h for h in hrefs if "/tools/" in h})
    print(len(hrefs),"tools")
    want=re.compile("img-to-vid|text-to-vid|wan-image|upscaler|removerized|object-remover|remove-people|online-ocr|paddleocr|ai-tts|thumbnai|2d-to-3d|background-remover|compress|text2video")
    for h in hrefs:
        if not want.search(h): continue
        q=b.new_page(); q.set_default_timeout(15000)
        try:
            q.goto(h,wait_until="commit",timeout=30000); q.wait_for_timeout(7000)
            fr=[f.url for f in q.frames if "hf.space" in f.url or ("toolfk" not in f.url and "http" in f.url and "google" not in f.url and "sharethis" not in f.url)]
            print(h.split("/")[-1],"->",fr[:2])
        except Exception as e: print(h,"ERR",str(e)[:60])
        q.close()
    b.close()
