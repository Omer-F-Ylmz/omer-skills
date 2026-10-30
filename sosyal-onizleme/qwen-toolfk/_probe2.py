from playwright.sync_api import sync_playwright
out="C:/Projeler/omer-skills/sosyal-onizleme/qwen-toolfk/"
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":800})
    pg.goto("https://chat.qwen.ai/",wait_until="domcontentloaded",timeout=45000)
    pg.wait_for_timeout(5000)
    # list clickable things
    for el in pg.query_selector_all("button, [role=button], [role=menuitem]")[:40]:
        t=(el.inner_text() or "").strip().replace("\n"," ")[:40]
        print("BTN",repr(t),el.get_attribute("aria-label"))
    ta=pg.query_selector("textarea")
    print("textarea",bool(ta))
    pg.screenshot(path=out+"qwen-ui.png")
    b.close()
