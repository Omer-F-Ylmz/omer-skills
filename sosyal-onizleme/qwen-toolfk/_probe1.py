import sys
from playwright.sync_api import sync_playwright
out="C:/Projeler/omer-skills/sosyal-onizleme/qwen-toolfk/"
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    for name,url in [("qwen","https://chat.qwen.ai/"),("toolfk","https://toolfk.com/")]:
        pg=b.new_page(viewport={"width":1280,"height":800})
        try:
            r=pg.goto(url,wait_until="domcontentloaded",timeout=45000)
            pg.wait_for_timeout(6000)
            print(name,r.status,pg.url,pg.title())
            pg.screenshot(path=out+f"{name}-home.png")
            print(pg.inner_text("body")[:1500].replace("\n"," | "))
        except Exception as e: print(name,"ERR",e)
    b.close()
