from playwright.sync_api import sync_playwright
out="C:/Projeler/omer-skills/sosyal-onizleme/qwen-toolfk/"
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":800})
    pg.goto("https://chat.qwen.ai/",wait_until="domcontentloaded",timeout=45000)
    pg.wait_for_timeout(5000)
    btns=pg.query_selector_all("button, [role=button], [role=menuitem]")
    btns[6].click(timeout=5000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=out+"qwen-mod.png")
    print(pg.inner_text("body")[:900].replace("\n"," | "))
    b.close()
