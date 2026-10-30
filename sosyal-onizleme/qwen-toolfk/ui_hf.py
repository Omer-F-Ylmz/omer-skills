import sys,time
from playwright.sync_api import sync_playwright
url,img,tag=sys.argv[1],sys.argv[2],sys.argv[3]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":1000}); pg.set_default_timeout(30000)
    pg.goto(url,wait_until="commit",timeout=60000); pg.wait_for_timeout(10000)
    fi=pg.query_selector_all("input[type=file]"); print("file inputs",len(fi))
    fi[0].set_input_files(img); pg.wait_for_timeout(3000)
    pg.screenshot(path=tag+"-1.png")
    print("btns",[x.inner_text().strip()[:20] for x in pg.query_selector_all("button")])
    btn=pg.get_by_role("button",name="Submit")
    t=time.time(); btn.first.click()
    for i in range(24):
        pg.wait_for_timeout(5000)
        body=pg.inner_text("body")
        if "Error" in body or "quota" in body.lower(): print("MSG",body[-300:].replace("\n"," | ")); break
        imgs=pg.query_selector_all("img")
        if i>2 and len(imgs)>=2: break
    print("sure",round(time.time()-t))
    pg.screenshot(path=tag+"-2.png",full_page=True)
    import base64
    for k,im in enumerate(pg.query_selector_all("img")):
        src=im.get_attribute("src") or ""
        if src.startswith("data:image"):
            ext="png" if "png" in src[:20] else "jpg"; open(f"{tag}-out{k}.{ext}","wb").write(base64.b64decode(src.split(",",1)[1])); print("SAVED",k,im.evaluate("e=>[e.naturalWidth,e.naturalHeight]"))
    b.close()
