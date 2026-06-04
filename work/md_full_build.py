import time, os, sys
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"
APP_NAME = "泡泡玛特深圳市场分析"
APPS_URL = "https://www.mingdao.com/app/my"

def ss(page, name):
    path = os.path.join(SC, f"md_{name}.png")
    page.screenshot(path=path)
    print(f"  [SCREENSHOT] {name}")

def wait_captcha(page, label=""):
    """Check captcha, return True if user solves it, raise if stuck"""
    js = """() => {
        const t = document.body.innerText || '';
        return t.includes('安全验证') || t.includes('拼图') || t.includes('拖动滑块');
    }"""
    has = page.evaluate(js)
    if has:
        print(f"\n*** CAPTCHA ({label}) - Please solve it in the browser window ***")
        for i in range(60):  # 120 seconds max
            time.sleep(2)
            still = page.evaluate(js)
            if not still:
                print("  Captcha solved! Continuing...")
                page.wait_for_timeout(2000)
                return True
            if i % 10 == 0:
                print(f"  ...{i*2}s (please solve the slider puzzle)")
        print("  ERROR: Captcha not solved in time")
        raise TimeoutError("Captcha timeout")
    return False

print("=" * 60)
print("Pop Mart Shenzhen - Mingdao Full Automation")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="msedge")
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        storage_state=SESSION
    )
    page = context.new_page()
    
    # === Step 1: Go to apps ===
    print("\n[1/6] Navigating to apps page...")
    try:
        page.goto(APPS_URL, wait_until="domcontentloaded", timeout=15000)
    except:
        print("  Navigation timeout, retrying...")
        page.goto(APPS_URL, wait_until="commit", timeout=30000)
    
    page.wait_for_timeout(3000)
    wait_captcha(page, "apps_page")
    ss(page, "01_apps")
    print(f"  Current URL: {page.url[:80]}")
    
    # Check if we're on login page (session expired)
    if "/login" in page.url or "login" in page.url.lower():
        print("\n  Session expired! Need fresh login.")
        print("  Opening login page...")
        page.goto("https://www.mingdao.com/login", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(2000)
        ss(page, "01b_login_needed")
        print("\n  >>> Please log in manually in the browser window <<<")
        print("  >>> After login, press Enter in this terminal to continue <<<")
        input("  Press Enter after login...")
        page.wait_for_timeout(3000)
        page.goto(APPS_URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        context.storage_state(path=SESSION)
        print("  Session saved!")
    
    # === Step 2: Find or create app ===
    print("\n[2/6] Checking if app exists...")
    app_found = page.evaluate("""() => (document.body.innerText||'').includes('泡泡玛特')""")
    print(f"  App '泡泡玛特' exists: {app_found}")
    
    if not app_found:
        print("  Creating new app...")
        # Find and click "新建应用"
        btns = page.evaluate("""() => {
            const r = [];
            const all = document.querySelectorAll('*');
            for (const el of all) {
                if (el.children.length === 0 && (el.textContent||'').trim() === '新建应用') {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0)
                        r.push({x: rect.x+rect.width/2, y: rect.y+rect.height/2});
                }
            }
            return r;
        }""")
        print(f"  Found {len(btns)} '新建应用' elements")
        
        if len(btns) >= 2:
            print(f"  Clicking 2nd button at ({btns[1]['x']:.0f}, {btns[1]['y']:.0f})")
            page.mouse.click(btns[1]['x'], btns[1]['y'])
        elif btns:
            page.mouse.click(btns[0]['x'], btns[0]['y'])
        else:
            print("  Trying alternative: locating by text...")
            try:
                page.locator("text=新建应用").last.click()
            except:
                pass
        
        page.wait_for_timeout(4000)
        wait_captcha(page, "app_create_dialog")
        ss(page, "02_create_dialog")
        
        # Fill app name in the popup
        print("  Filling app name...")
        try:
            # Find the input field in the dialog
            inp = page.locator("input:visible").first
            inp.click()
            page.wait_for_timeout(300)
            inp.fill("")
            page.wait_for_timeout(200)
            inp.fill(APP_NAME)
            print(f"  Filled: {APP_NAME}")
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f"  Fill attempt 1 failed: {e}")
            # Try alternative: find input by role
            try:
                inp = page.locator('[role="dialog"] input, .ant-modal input, [class*=modal] input').first
                inp.click()
                inp.fill(APP_NAME)
                print(f"  Filled via alt method")
            except Exception as e2:
                print(f"  All fill attempts failed. Please type '{APP_NAME}' manually in the dialog.")
                print("  >>> Press Enter here after typing the app name <<<")
                input("  Press Enter...")
        
        ss(page, "03_name_filled")
        
        # Click confirm button
        print("  Clicking confirm...")
        try:
            # Try Enter key first
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)
        except:
            pass
        
        # Check if dialog is still open - if so, find and click button
        still_open = page.evaluate("""() => {
            const modals = document.querySelectorAll('.ant-modal-wrap, .ant-modal, [class*=modal], [role=dialog]');
            for (const m of modals) {
                const r = m.getBoundingClientRect();
                if (r.width > 50 && r.height > 50) return true;
            }
            return false;
        }""")
        
        if still_open:
            print("  Dialog still open, looking for confirm button...")
            btn_found = page.evaluate("""() => {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    const t = (b.textContent||'').trim();
                    if (['确定','创建','保存','OK','确认','提交'].some(kw => t.includes(kw))) {
                        const r = b.getBoundingClientRect();
                        return {text: t, x: r.x+r.width/2, y: r.y+r.height/2};
                    }
                }
                return null;
            }""")
            if btn_found:
                print(f"  Clicking '{btn_found['text']}'")
                page.mouse.click(btn_found['x'], btn_found['y'])
        
        page.wait_for_timeout(5000)
        wait_captcha(page, "after_create")
    
    # === Step 3: Enter the app ===
    print("\n[3/6] Entering the app...")
    ss(page, "04_before_enter")
    
    # Reload apps page to be sure
    if "app/my" not in page.url:
        page.goto(APPS_URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
    
    # Find and click the app
    try:
        app_link = page.locator("text=泡泡玛特").first
        if app_link.is_visible(timeout=5000):
            app_link.click()
            page.wait_for_timeout(5000)
            print(f"  Entered app at: {page.url[:80]}")
    except Exception as e:
        print(f"  Click failed: {e}")
        print("  Please click '泡泡玛特深圳市场分析' manually in the browser.")
        print("  >>> Press Enter after clicking <<<")
        input("  Press Enter...")
    
    wait_captcha(page, "inside_app")
    ss(page, "05_inside_app")
    
    # === Step 4: Check worksheets ===
    print("\n[4/6] Checking worksheets...")
    app_state = page.evaluate("""() => {
        const body = document.body.innerText || '';
        return {
            has_store: body.includes('门店数据'),
            has_staff: body.includes('人员开支'),
            has_product: body.includes('商品销售'),
            has_revenue: body.includes('应收明细'),
            has_dashboard: body.includes('驾驶舱') || body.includes('仪表盘'),
            url: window.location.href,
            text: body.substring(0, 600)
        };
    }""")
    
    for k, v in app_state.items():
        if k != 'text':
            print(f"  {k}: {v}")
    print(f"  Page preview: {app_state['text'][:300]}")
    
    # Need to create worksheets if they don't exist
    worksheets_needed = []
    if not app_state['has_store']: worksheets_needed.append('门店数据')
    if not app_state['has_staff']: worksheets_needed.append('人员开支')
    if not app_state['has_product']: worksheets_needed.append('商品销售')
    if not app_state['has_revenue']: worksheets_needed.append('应收明细')
    
    if worksheets_needed:
        print(f"\n  Worksheets to create: {worksheets_needed}")
        print("  >>> TODO: Create worksheets with proper fields <<<")
        print("  >>> This requires navigating Mingdao's worksheet creation UI <<<")
    
    # Save state
    ss(page, "06_state_check")
    
    # === Step 5: Create worksheets if needed ===
    if worksheets_needed:
        print("\n[5/6] Creating worksheets...")
        print("  Looking for '新建工作表' or '+' button...")
        
        # Try to find the create worksheet button
        create_info = page.evaluate("""() => {
            const results = [];
            const all = document.querySelectorAll('*');
            for (const el of all) {
                const t = (el.textContent||'').trim();
                if (['新建工作表','新建','+ 新建','添加工作表','创建表'].some(kw => t.includes(kw)) && el.children.length <= 2) {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0) results.push({text: t, x: r.x+r.width/2, y: r.y+r.height/2});
                }
            }
            return results;
        }""")
        
        print(f"  Found {len(create_info)} create buttons")
        for ci in create_info:
            print(f"    '{ci['text']}' at ({ci['x']:.0f}, {ci['y']:.0f})")
        
        if not create_info:
            print("\n  >>> Unable to find worksheet creation button automatically <<<")
            print("  >>> Please manually create these worksheets in Mingdao: <<<")
            for ws in worksheets_needed:
                print(f"      - {ws}")
            print("\n  Each worksheet should have appropriate fields for Pop Mart data.")
            print("  After creating them, press Enter to continue...")
            input("  Press Enter...")
    
    # Save session
    context.storage_state(path=SESSION)
    print("\n[6/6] Session saved.")
    
    print("\n" + "=" * 60)
    print("Automation paused. Browser will stay open for 5 minutes.")
    print("You can work in the browser. Press Ctrl+C to close.")
    print("=" * 60)
    
    try:
        time.sleep(300)
    except KeyboardInterrupt:
        pass
    
    browser.close()
    print("Done!")
