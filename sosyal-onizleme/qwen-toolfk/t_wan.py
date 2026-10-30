import time,base64
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":1400}); pg.set_default_timeout(30000)
    pg.goto("https://zerogpu-aoti-wan2-2-fp8da-aoti-faster.hf.space/",wait_until="commit",timeout=60000); pg.wait_for_timeout(12000)
    pg.query_selector_all("input[type=file]")[0].set_input_files("test-tilki-kucuk.jpg"); pg.wait_for_timeout(3000)
    tb=pg.query_selector_all("textarea"); print("textareas",len(tb))
    if tb: tb[0].fill("the blue fox waves its paw and smiles, gentle head movement")
    print("btns",[x.inner_text().strip()[:25] for x in pg.query_selector_all("button")])
    pg.screenshot(path="wan-1.png",full_page=True)
    pg.get_by_role("button",name="Generate Video").first.click()
    t=time.time()
    for i in range(40):
        pg.wait_for_timeout(5000)
        v=pg.query_selector("video")
        body=pg.inner_text("body")
        if v and v.get_attribute("src"): print("VIDEO",v.get_attribute("src")[:150]); break
        if "quota" in body.lower() or "Error" in body: print("MSG",[l for l in body.split("\n") if "uota" in l or "rror" in l][:3]); break
    print("sure",round(time.time()-t))
    pg.screenshot(path="wan-2.png",full_page=True)
    v=pg.query_selector("video")
    if v:
        src=v.get_attribute("src"); r=pg.request.get(src); open("out-wan.mp4","wb").write(r.body()); print("saved",len(r.body()))
    b.close()
