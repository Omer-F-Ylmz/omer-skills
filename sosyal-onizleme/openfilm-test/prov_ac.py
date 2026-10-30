import sys, os
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8")
url = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(4000)
    pg.mouse.click(40, 24)
    pg.wait_for_timeout(1500)
    pg.get_by_text("Providers", exact=True).first.click()
    pg.wait_for_timeout(1000)
    t = pg.get_by_text("fal.ai", exact=True).first
    t.scroll_into_view_if_needed()
    t.locator("xpath=../../..").get_by_role("button", name="Connect").click()
    pg.wait_for_timeout(800)
    inp = pg.locator("input[type=password]:visible, input[type=text]:visible").last
    print(inp.get_attribute("placeholder"))
    inp.fill(os.environ["FAL_KEY"])
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(3000)
    t.scroll_into_view_if_needed()
    pg.screenshot(path="prov5.png")
    b.close()
