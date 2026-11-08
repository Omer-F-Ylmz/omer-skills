from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    for s in ["ai-object-remover","ai-2d-to-3d-image-converter","ai-youtube-thumbnail-maker","online-ocr","ai-tts"]:
        pg=b.new_page(); pg.set_default_timeout(15000)
        try:
            pg.goto("https://www.toolfk.com/tools/"+s+".html",wait_until="commit",timeout=40000); pg.wait_for_timeout(7000)
            print(s,[x.inner_text().strip()[:30] for x in pg.query_selector_all("button") if x.is_visible()][:12],
                  "files",len(pg.query_selector_all("input[type=file]")),"frames",[f.url[:60] for f in pg.frames[1:4]])
        except Exception as e: print(s,"ERR",str(e)[:60])
        pg.close()
    b.close()
