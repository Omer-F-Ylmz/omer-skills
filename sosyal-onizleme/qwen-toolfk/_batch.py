from playwright.sync_api import sync_playwright
S="ai-2d-to-3d-image-converter ai-background-remover ai-object-remover ai-remove-people-from-photos ai-tts ai-youtube-thumbnail-maker online-images-compression online-img-to-video online-text-to-video online-ocr".split()
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    for s in S:
        q=b.new_page(viewport={"width":1280,"height":900}); q.set_default_timeout(15000)
        try:
            q.goto("https://www.toolfk.com/tools/"+s+".html",wait_until="commit",timeout=40000); q.wait_for_timeout(9000)
            fr=[f for f in q.frames if f!=q.main_frame and not any(k in f.url for k in("google","sharethis","about:","data:","doubleclick"))]
            print("##",s,"iframes",[f.url[:70] for f in fr])
            tgt=fr[0] if fr else q.main_frame
            print(" files",len(tgt.query_selector_all("input[type=file]")),"ta",len(tgt.query_selector_all("textarea")),"btns",[x.inner_text().strip()[:18] for x in tgt.query_selector_all("button")][:10])
            q.screenshot(path=s+"-page.png")
            body=q.inner_text("body"); i=body.find("Loading tool"); print(" ",body[300:620].replace("\n"," | "))
        except Exception as e: print("##",s,"ERR",str(e)[:80])
        q.close()
    b.close()
