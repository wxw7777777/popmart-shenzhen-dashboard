import time, os, sys
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"
APP_NAME = "泡泡玛特深圳市场分析"
APPS_URL = "https://www.mingdao.com/app/my"

def ss(page, name):
    page.screenshot(path=os.path.join(SC, f"md_{name}.png"))
    print(f"  [SCREENSHOT] {name}")

def wait_captcha(page, label=""):
    captcha_js = """() => {
        const t = document.body.innerText || '';
        return t.includes('安全验证') || t.includes('拼图') || t.includes('拖动滑块');
    }"""
    has = page.evaluate(captcha_js)
    if has:
        print(f"\n*** CAPTCHA ({label}) - Please solve in browser ***")
        print("Waiting 60s...")
        for i in range(30):
            time.sleep(2)
            still = page.evaluate(captcha_js)
            if not still:
                print("  Captcha solved!")
                page.wait_for_timeout(2000)
                return True
            if i % 5 == 0:
                print(f"  ...{i*2}s")
    return has

print("=" * 60)
print("Pop Mart Shenzhen - Mingdao Automation")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="msedge")
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        storage_state=SESSION
    )
    page = context.new_page()
    
    print("\n[1] Opening apps page...")
    page.goto(APPS_URL, wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(3000)
    wait_captcha(page, "apps")
    ss(page, "01_apps")
    print(f"  URL: {page.url}")
    
    print("\n[2] Checking for Pop Mart app...")
    app_found = page.evaluate("""() => (document.body.innerText||'').includes('泡泡玛特')""")
    print(f"  App exists: {app_found}")
    
    if app_found:
        print("  Clicking into app...")
        try:
            el = page.locator("text=泡泡玛特").first
            if el.is_visible(timeout=5000):
                el.click()
                page.wait_for_timeout(5000)
                print(f"  Entered: {page.url}")
        except Exception as e:
            print(f"  Click failed: {e}")
    else:
        print("  App NOT found, creating...")
        btns = page.evaluate("""() => {
            const r = [];
            const w = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
            let n;
            while (n = w.nextNode()) {
                if ((n.textContent||'').trim()==='新建应用' && n.children.length===0) {
                    const rect = n.getBoundingClientRect();
                    if (rect.width>0) r.push({x:rect.x+rect.width/2, y:rect.y+rect.height/2});
                }
            }
            return r;
        }""")
        print(f"  Found {len(btns)} 'new app' buttons")
        if len(btns) >= 2:
            page.mouse.click(btns[1]["x"], btns[1]["y"])
        elif btns:
            page.mouse.click(btns[0]["x"], btns[0]["y"])
        page.wait_for_timeout(4000)
        wait_captcha(page, "dialog")
        
        try:
            inp = page.locator("input:visible").first
            inp.click()
            inp.fill("")
            page.wait_for_timeout(200)
            inp.fill(APP_NAME)
            print(f"  Filled: {APP_NAME}")
        except Exception as e:
            print(f"  Fill failed: {e}")
        
        ss(page, "02_dialog")
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
        wait_captcha(page, "after_create")
    
    ss(page, "03_inside")
    
    print("\n[3] Checking app contents...")
    state = page.evaluate("""() => {
        const body = document.body.innerText || '';
        return {
            store: body.includes('门店数据'),
            staff: body.includes('人员开支'),
            product: body.includes('商品销售'),
            revenue: body.includes('应收明细'),
            dash: body.includes('驾驶舱'),
            url: window.location.href,
            text: body.substring(0, 500)
        };
    }""")
    for k, v in state.items():
        if k != "text":
            print(f"  {k}: {v}")
    print(f"  Page text: {state['text'][:300]}")
    
    context.storage_state(path=SESSION)
    print("\nSession saved. Browser will stay open 300s...")
    try:
        time.sleep(300)
    except KeyboardInterrupt:
        pass
    browser.close()
    print("Done!")
