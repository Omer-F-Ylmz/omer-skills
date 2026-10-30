import sys,time,base64
from playwright.sync_api import sync_playwright
slug,btn,prompt,wait=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4])
img=sys.argv[5] if len(sys.argv)>5 else "test-tilki-kucuk.jpg"
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":1300}); pg.set_default_timeout(20000)
    nets=[]
    pg.on("response",lambda r: nets.append((r.status,r.url[:90])) if "toolfk" in r.url and r.request.method=="POST" else None)
    pg.goto("https://www.toolfk.com/tools/"+slug+".html",wait_until="commit",timeout=40000); pg.wait_for_timeout(8000)
    fi=pg.query_selector_all("input[type=file]")
    if fi and img!="-": fi[0].set_input_files(img); pg.wait_for_timeout(2500)
    ta=[t for t in pg.query_selector_all("textarea") if t.is_visible()]
    if ta and prompt!="-": ta[0].fill(prompt)
    pg.evaluate("document.querySelectorAll('.fc-consent-root,.fc-dialog-overlay,.fc-message-root').forEach(e=>e.remove())")
    pg.get_by_role("button",name=btn).first.click()
    t=time.time()
    for i in range(wait//5):
        pg.wait_for_timeout(5000)
        body=pg.inner_text("body")
        if i>1 and "Generating" not in body and not pg.query_selector("text=Dream big"): break
    print("sure",round(time.time()-t))
    pg.screenshot(path=slug+"-sonuc.png",full_page=False)
    hits=[l.strip() for l in pg.inner_text("body").split("\n") if any(k in l.lower() for k in("limit","quota","credit","failed","error","log in to","sign in","wait","queue"))]
    print("MSG",hits[:6]); print("NET",nets[-5:])
    for k,im in enumerate(pg.query_selector_all("img")):
        s=im.get_attribute("src") or ""
        if s.startswith("data:image") and im.evaluate("e=>e.naturalWidth")>200:
            open(f"{slug}-out{k}.png","wb").write(base64.b64decode(s.split(",",1)[1])); print("SAVED",k)
    v=pg.query_selector("video[src]")
    if v: print("VIDEO",v.get_attribute("src")[:140])
    b.close()
