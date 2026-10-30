from playwright.sync_api import sync_playwright
out="C:/Projeler/omer-skills/sosyal-onizleme/qwen-toolfk/"
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome",headless=True)
    pg=b.new_page(viewport={"width":1280,"height":800}); pg.set_default_timeout(20000)
    pg.goto("https://www.toolfk.com/",wait_until="commit",timeout=40000)
    pg.wait_for_timeout(6000)
    links=pg.eval_on_selector_all("a","els=>els.map(e=>[e.innerText.trim().slice(0,40),e.href])")
    seen=set()
    for t,h in links:
        if h not in seen and t: seen.add(h); print(t,"|",h)
    b.close()
