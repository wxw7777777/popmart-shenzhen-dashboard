"""Mingdao - create Pop Mart application via Playwright"""
import json, time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
DASHBOARD = "https://www.mingdao.com/dashboard"
SCREENSHOTS = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"

def screenshot(page, name):
    path = os.path.join(SCREENSHOTS, f"md_{name}.png")
    page.screenshot(path=path, full_page=False)
    print(f"  Screenshot: {path}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        storage_state=SESSION
    )
    page = context.new_page()
    
    # Step 1: Go to dashboard
    print("1. Navigating to dashboard...")
    page.goto(DASHBOARD, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)
    screenshot(page, "step1_dashboard")
    
    # Step 2: Find and click 应用 in nav
    print("2. Looking for 应用 nav button...")
    nav_texts = page.evaluate("""() => {
        const nav = document.querySelectorAll('nav a, nav button, .nav-item, [class*="nav"] a, [class*="Nav"] a, .menu-item, [class*="menu"] span, .sidebar a, [class*="sidebar"] span, .ant-menu-item');
        return Array.from(nav).map(el => ({text: el.textContent.trim().substring(0,20), tag: el.tagName, class: el.className?.substring(0,50) || ''}));
    }""")
    for item in nav_texts[:30]:
        print(f"  Nav: [{item['tag']}] {item['text']} | {item['class']}")
    
    # Try various selectors for 应用
    selectors = [
        "text=应用",
        "a:has-text('应用')",
        "span:has-text('应用')",
        "li:has-text('应用')",
        "[class*='nav']:has-text('应用')",
        ".ant-menu-item:has-text('应用')",
        "div:has-text('应用') >> nth=0",
    ]
    
    clicked = False
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=1000):
                print(f"  Found with: {sel}")
                el.click()
                page.wait_for_timeout(3000)
                screenshot(page, "step2_after_app_click")
                clicked = True
                break
        except:
            continue
    
    if not clicked:
        print("  Trying broader search...")
        # Get all clickable elements
        all_text = page.evaluate("""() => {
            const els = document.querySelectorAll('a, button, span, div, li');
            return Array.from(els).filter(el => {
                const t = el.textContent.trim();
                return t.includes('应用') || t.includes('APP') || t.includes('app');
            }).map(el => ({
                text: el.textContent.trim().substring(0,30),
                tag: el.tagName,
                class: el.className?.substring(0,60) || '',
                id: el.id || ''
            }));
        }""")
        for item in all_text[:20]:
            print(f"  Found: [{item['tag']}#{item['id']}] {item['text']} | {item['class']}")
    
    # Step 3: After entering apps, look for create button
    print("3. Looking for create/new app button...")
    page.wait_for_timeout(2000)
    
    create_selectors = [
        "text=新建应用",
        "text=创建应用",
        "text=新建",
        "button:has-text('创建')",
        "button:has-text('新建')",
        "a:has-text('新建应用')",
        "span:has-text('新建应用')",
        "[class*='create']",
        "[class*='add']",
        ".ant-btn-primary:has-text('新建')",
    ]
    
    for sel in create_selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=1000):
                print(f"  Found create button: {sel}")
                el.click()
                page.wait_for_timeout(3000)
                screenshot(page, "step3_create_dialog")
                break
        except:
            continue
    
    # Step 4: Check current page state
    print("4. Page URL:", page.url)
    print("5. Page title:", page.title())
    
    # Dump visible buttons
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button, a.btn, [role="button"]')).filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0;
        }).map(el => ({
            text: el.textContent.trim().substring(0,30),
            class: el.className?.substring(0,50) || ''
        }));
    }""")
    print("  Visible buttons:")
    for b in btns[:20]:
        print(f"    [{b['class'][:30]}] {b['text']}")
    
    page.wait_for_timeout(3000)
    browser.close()
    print("Done.")
