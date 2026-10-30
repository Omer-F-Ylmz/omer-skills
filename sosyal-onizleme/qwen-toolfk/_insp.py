import sys
from playwright.sync_api import sync_playwright
slug=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":900}); pg.set_default_timeout(20000)
    pg.goto("https://www.toolfk.com/tools/"+slug+".html",wait_until="commit",timeout=40000)
    pg.wait_for_timeout(9000)
    print("URL",pg.url)
    for f in pg.frames: print("FRAME",f.url[:120])
    for fr in pg.frames:
        ins=fr.query_selector_all("input[type=file]")
        print(fr.url[:60],"files",len(ins),"btns",[ (x.inner_text() or "").strip()[:25] for x in fr.query_selector_all("button")][:15])
        print("TEXTAREA",len(fr.query_selector_all("textarea")))
    pg.screenshot(path=slug+"-page.png")
    print(pg.inner_text("body")[:700].replace("\n"," | "))
    b.close()
