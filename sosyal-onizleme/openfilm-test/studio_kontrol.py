import sys
from playwright.sync_api import sync_playwright
url = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(6000)
    pg.screenshot(path="studio.png")
    print(pg.title(), pg.url)
    b.close()
