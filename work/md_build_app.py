"""Create Pop Mart app in Mingdao"""
import time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"
DASHBOARD = "https://www.mingdao.com/dashboard"

def ss(page, name):
    page.screenshot(path=os.path.join(SC, f"md_{name}.png"))
    print(f"  [SCREENSHOT] {name}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width":1440,"height":900}, storage_state=SESSION)
    page = context.new_page()
    
    # Step 1: Go to dashboard
    print("1. Going to dashboard...")
    page.goto(DASHBOARD, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    ss(page, "01_dashboard")
    
    # Dump all visible nav elements
    print("2. Scanning navigation...")
    nav = page.evaluate("""() => {
        const items = [];
        document.querySelectorAll('a, button, span, div, li').forEach(el => {
            const t = el.textContent.trim();
            if (t && t.length < 30 && el.offsetParent !== null) {
                const rect = el.getBoundingClientRect();
                if (rect.width > 10 && rect.height > 10 && rect.top < 200) {
                    items.push({
                        text: t,
                        tag: el.tagName,
                        x: Math.round(rect.x),
                        y: Math.round(rect.y),
                        w: Math.round(rect.width),
                        cls: (el.className?.toString() || '').substring(0,60)
                    });
                }
            }
        });
        return items.slice(0,40);
    }""")
    
    for item in nav:
        print(f"  [{item['tag']}] ({item['x']},{item['y']}) {item['text'][:30]} | {item['cls'][:40]}")
    
    # Step 3: Click "应用" in nav
    print("\n3. Clicking 应用...")
    app_clicked = False
    
    # Try clicking by text content first
    app_selectors = [
        "text=应用",
        "span:has-text('应用')",
        "a:has-text('应用')",
        "div:has-text('应用')",
        "li:has-text('应用')",
        "[class*=nav]:has-text('应用')",
    ]
    
    for sel in app_selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=2000):
                print(f"  Found: {sel}")
                el.click()
                page.wait_for_timeout(3000)
                ss(page, "02_after_app_click")
                app_clicked = True
                break
        except:
            continue
    
    if not app_clicked:
        # Try clicking by position from the nav scan results
        for item in nav:
            if '应用' in item['text']:
                print(f"  Clicking by position: ({item['x']},{item['y']})")
                page.mouse.click(item['x'] + item['w']//2, item['y'] + 10)
                page.wait_for_timeout(3000)
                ss(page, "02_after_app_click_pos")
                app_clicked = True
                break
    
    if not app_clicked:
        print("  ERROR: Could not find 应用 button!")
        browser.close()
        exit(1)
    
    # Step 4: Look for create app button
    print("\n4. Looking for create/new app button...")
    page.wait_for_timeout(2000)
    ss(page, "03_app_page")
    
    # Dump visible buttons
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button, a, span, div[role=button]')).filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 20 && rect.height > 10 && el.offsetParent !== null;
        }).map(el => ({
            text: el.textContent.trim().substring(0,40),
            tag: el.tagName,
            cls: (el.className?.toString()||'').substring(0,60)
        }));
    }""")
    
    print("  Visible interactive elements:")
    for b in btns[:30]:
        print(f"    [{b['tag']}] {b['text']} | {b['cls'][:40]}")
    
    create_selectors = [
        "text=新建应用",
        "text=创建应用", 
        "text=新建",
        "text=创建",
        "button:has-text('新建')",
        "button:has-text('创建')",
        "a:has-text('新建应用')",
        "span:has-text('新建应用')",
        "[class*=create]",
        "[class*=add]",
        ".ant-btn-primary",
    ]
    
    created = False
    for sel in create_selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=1000):
                print(f"  Found: {sel}")
                el.click()
                page.wait_for_timeout(2000)
                ss(page, "04_create_dialog")
                created = True
                break
        except:
            continue
    
    if not created:
        print("  Checking for '+' icon or create button by position...")
        # Try clicking common positions for add buttons (top right or bottom right)
        vw = page.viewport_size
        if vw:
            # Try top right corner
            for tx in [vw['width']-100, vw['width']-200, vw['width']-300]:
                page.mouse.click(tx, 80)
                page.wait_for_timeout(1000)
    
    ss(page, "05_current_state")
    print(f"  Current URL: {page.url}")
    
    page.wait_for_timeout(5000)
    browser.close()
    print("\nDone.")
