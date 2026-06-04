"""Create Pop Mart app in Mingdao - v2 with better dialog handling"""
import time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"

def ss(page, name):
    page.screenshot(path=os.path.join(SC, f"md_{name}.png"))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width":1440,"height":900}, storage_state=SESSION)
    page = context.new_page()
    
    # Go to apps page directly
    print("1. Going to app page...")
    page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    ss(page, "v2_01_app_page")
    
    # Find the 新建应用 button and get exact coordinates
    print("2. Finding 新建应用 button...")
    btn_info = page.evaluate("""() => {
        const els = document.querySelectorAll('span, button, a, div');
        for (const el of els) {
            if (el.textContent.trim() === '新建应用' || el.textContent.includes('新建应用')) {
                const rect = el.getBoundingClientRect();
                return {
                    text: el.textContent.trim(),
                    tag: el.tagName,
                    x: rect.x + rect.width/2,
                    y: rect.y + rect.height/2,
                    w: rect.width,
                    h: rect.height,
                    cls: el.className?.toString() || ''
                };
            }
        }
        return null;
    }""")
    
    if btn_info:
        print(f"  Button: [{btn_info['tag']}] '{btn_info['text']}' at ({btn_info['x']:.0f},{btn_info['y']:.0f}) class='{btn_info['cls']}'")
        
        # First try clicking the specific span
        try:
            el = page.locator(f"span:has-text('新建应用')").last
            if el.is_visible():
                print("  Clicking span:has-text('新建应用')")
                el.click(force=True)
                page.wait_for_timeout(3000)
        except Exception as e:
            print(f"  Span click failed: {e}")
            # Try click by coordinates
            print(f"  Clicking by coordinates: ({btn_info['x']:.0f},{btn_info['y']:.0f})")
            page.mouse.click(btn_info['x'], btn_info['y'])
            page.wait_for_timeout(3000)
    else:
        print("  NOT FOUND!")
    
    ss(page, "v2_02_after_click")
    
    # Check for any modal/dialog
    print("3. Checking for modal...")
    modal_info = page.evaluate("""() => {
        const modals = document.querySelectorAll('[class*=modal], [class*=Modal], [class*=dialog], [class*=Dialog], [class*=drawer], [class*=Drawer], .ant-modal, .ant-drawer');
        const result = [];
        modals.forEach(m => {
            const rect = m.getBoundingClientRect();
            if (rect.width > 0) {
                result.push({
                    class: m.className?.toString().substring(0,100),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height),
                    visible: m.offsetParent !== null,
                    text: m.textContent?.substring(0,100) || ''
                });
            }
        });
        return result;
    }""")
    
    for m in modal_info:
        print(f"  Modal: {m['class'][:60]} | {m['w']}x{m['h']} | vis={m['visible']}")
        print(f"    Text: {m['text'][:80]}")
    
    # If no modal found, try clicking the newAppBtn class directly
    if not modal_info:
        print("  No modal found, trying .newAppBtn class...")
        try:
            el = page.locator(".newAppBtn").first
            if el.is_visible():
                print("  Found .newAppBtn, clicking...")
                el.click()
                page.wait_for_timeout(3000)
                ss(page, "v2_03_newappbtn_click")
        except Exception as e:
            print(f"  .newAppBtn click failed: {e}")
    
    # Check again for modal
    modal_info2 = page.evaluate("""() => {
        const modals = document.querySelectorAll('[class*=modal], [class*=Modal], [class*=dialog], [class*=Dialog], [class*=drawer], [class*=Drawer], .ant-modal, .ant-drawer');
        const result = [];
        modals.forEach(m => {
            const rect = m.getBoundingClientRect();
            if (rect.width > 0) {
                result.push({
                    class: m.className?.toString().substring(0,100),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height),
                    visible: m.offsetParent !== null
                });
            }
        });
        return result;
    }""")
    
    for m in modal_info2:
        print(f"  Modal2: {m['class'][:60]} | {m['w']}x{m['h']} | vis={m['visible']}")
    
    # Get ALL inputs now
    inputs = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('input, textarea')).map(el => ({
            type: el.type || el.tagName,
            placeholder: el.placeholder || '',
            name: el.name || '',
            id: el.id || '',
            cls: (el.className?.toString()||'').substring(0,60),
            visible: el.offsetParent !== null,
            rect: (()=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};})()
        }));
    }""")
    
    print(f"\n4. All inputs ({len(inputs)}):")
    for inp in inputs:
        if inp['visible']:
            print(f"  [{inp['type']}] placeholder='{inp['placeholder']}' name='{inp['name']}' | {inp['cls'][:40]}")
    
    ss(page, "v2_04_final")
    
    page.wait_for_timeout(5000)
    browser.close()
    print("\nDone.")
