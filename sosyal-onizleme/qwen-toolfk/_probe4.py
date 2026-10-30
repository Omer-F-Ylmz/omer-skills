import re,sys
from playwright.sync_api import sync_playwright
out="C:/Projeler/omer-skills/sosyal-onizleme/qwen-toolfk/"
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":800})
    reqs=[]
    pg.on("response",lambda r: reqs.append((r.status,r.url[:110])) if "qwen" in r.url and r.request.method=="POST" else None)
    pg.goto("https://chat.qwen.ai/",wait_until="domcontentloaded",timeout=45000)
    pg.wait_for_timeout(5000)
    pg.query_selector_all("button, [role=button], [role=menuitem]")[6].click()
    pg.wait_for_timeout(1000)
    pg.get_by_text(re.compile("Video Olu")).first.click()
    pg.wait_for_timeout(1500)
    pg.screenshot(path=out+"qwen-videomod.png")
    ta=pg.query_selector("textarea")
    ta.fill("A small orange fox mascot waves at the camera in a sunny meadow, cinematic, 5 seconds")
    pg.keyboard.press("Enter")
    for i in range(12):
        pg.wait_for_timeout(10000)
        txt=pg.inner_text("body")
        print(i*10, pg.url[-40:], len(txt), txt[-200:].replace("\n"," | "))
        if "video" in pg.content().lower() and pg.query_selector("video"): print("VIDEO EL"); break
    pg.screenshot(path=out+"qwen-video-sonuc.png")
    for r in reqs[-15:]: print(r)
    b.close()
