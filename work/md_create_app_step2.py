"""Step 2: Fill in app creation dialog and create the Pop Mart app"""
import time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"
APP_URL = "https://www.mingdao.com/app/my"

def ss(page, name):
    page.screenshot(path=os.path.join(SC, f"md_{name}.png"))
    print(f"  [SCREENSHOT] {name}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width":1440,"height":900}, storage_state=SESSION)
    page = context.new_page()
    
    print("1. Going to app page...")
    page.goto(APP_URL, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    ss(page, "s2_01_app_page")
    
    print("2. Clicking 新建应用...")
    # Try multiple selectors
    clicked = False
    for sel in ["text=新建应用", "span:has-text('新建应用')", ".newAppBtn", "[class*=newApp]"]:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=2000):
                print(f"  Clicking: {sel}")
                el.click()
                page.wait_for_timeout(3000)
                ss(page, "s2_02_dialog")
                clicked = True
                break
        except:
            continue
    
    if not clicked:
        print("  ERROR: Could not click 新建应用")
        browser.close()
        exit(1)
    
    # Step 3: Fill in the dialog
    print("3. Looking for dialog inputs...")
    
    # Check what dialog elements exist
    dialog_info = page.evaluate("""() => {
        const inputs = document.querySelectorAll('input, textarea, select');
        const result = [];
        inputs.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                result.push({
                    type: el.type || el.tagName,
                    placeholder: el.placeholder || '',
                    name: el.name || '',
                    value: el.value || '',
                    id: el.id || '',
                    cls: (el.className?.toString()||'').substring(0,50),
                    visible: el.offsetParent !== null
                });
            }
        });
        return result;
    }""")
    
    for inp in dialog_info[:20]:
        print(f"  Input: type={inp['type']} placeholder='{inp['placeholder']}' name='{inp['name']}' visible={inp['visible']}")
    
    # Find and fill app name
    print("\n4. Filling app name: 泡泡玛特深圳市场分析")
    name_filled = False
    
    # Try common input selectors
    name_selectors = [
        "input[placeholder*=名称]",
        "input[placeholder*=应用名]",
        "input[name*=name]",
        "input[name*=appName]",
        "input[name*=title]",
        ".ant-modal input",
        "[class*=modal] input",
        "[class*=dialog] input",
        "input:visible",
    ]
    
    for sel in name_selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=1000):
                print(f"  Found input: {sel}")
                el.click()
                el.fill("")
                el.fill("泡泡玛特深圳市场分析")
                page.wait_for_timeout(1000)
                ss(page, "s2_03_name_filled")
                name_filled = True
                break
        except:
            continue
    
    if not name_filled:
        # Try filling by type=text inputs
        text_inputs = page.locator("input[type=text]:visible")
        count = text_inputs.count()
        print(f"  Found {count} visible text inputs")
        if count > 0:
            text_inputs.first.click()
            text_inputs.first.fill("")
            text_inputs.first.fill("泡泡玛特深圳市场分析")
            page.wait_for_timeout(1000)
            ss(page, "s2_03_name_filled_v2")
            name_filled = True
    
    if not name_filled:
        print("  WARNING: Could not fill app name automatically")
    
    # Step 5: Click confirm/submit button
    print("\n5. Looking for confirm button...")
    confirm_selectors = [
        "button:has-text('确定')",
        "button:has-text('创建')",
        "button:has-text('保存')",
        "button:has-text('提交')",
        "button:has-text('确认')",
        ".ant-btn-primary",
        "[class*=primary]",
        "button[type=submit]",
        ".ant-modal button:last-child",
    ]
    
    confirmed = False
    for sel in confirm_selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=1000):
                txt = el.text_content() or ''
                print(f"  Found: {sel} text='{txt[:20]}'")
                el.click()
                page.wait_for_timeout(4000)
                ss(page, "s2_04_after_confirm")
                confirmed = True
                break
        except:
            continue
    
    if not confirmed:
        # Dump all visible buttons
        all_btns = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('button, [role=button]')).filter(el => {
                return el.offsetParent !== null;
            }).map(el => ({
                text: el.textContent.trim().substring(0,30),
                cls: (el.className?.toString()||'').substring(0,50)
            }));
        }""")
        print("  All visible buttons:")
        for b in all_btns[:15]:
            print(f"    '{b['text']}' | {b['cls'][:40]}")
    
    print(f"\n6. Current URL: {page.url}")
    ss(page, "s2_05_final")
    
    page.wait_for_timeout(5000)
    browser.close()
    print("Done.")
