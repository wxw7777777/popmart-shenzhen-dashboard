"""Mingdao app creator - handles captcha by giving user time to solve it"""
import time, os, sys
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"
APP_NAME = "泡泡玛特深圳市场分析"
APPS_URL = "https://www.mingdao.com/app/my"

def ss(page, name):
    path = os.path.join(SC, f"md4_{name}.png")
    page.screenshot(path=path)
    print(f"  [SCREENSHOT] {name}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        storage_state=SESSION
    )
    page = context.new_page()
    
    print("=" * 60)
    print("Step 1: Opening apps page...")
    print("=" * 60)
    page.goto(APPS_URL, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    ss(page, "01_apps")
    
    print(f"URL: {page.url}")
    print(f"Title: {page.title()}")
    
    # Check for captcha and give user time
    has_captcha = page.evaluate("""() => {
        const text = document.body.innerText;
        return text.includes('安全验证') || text.includes('拼图') || text.includes('拖动');
    }""")
    
    if has_captcha:
        print("\n*** CAPTCHA DETECTED! ***")
        print("Please solve the captcha in the browser window...")
        print("You have 30 seconds. After solving, the script will continue.")
        for i in range(15):
            time.sleep(2)
            still_captcha = page.evaluate("""() => {
                return document.body.innerText.includes('安全验证');
            }""")
            if not still_captcha:
                print("  Captcha solved! Continuing...")
                break
            if i % 3 == 0:
                print(f"  Waiting... {i*2}s")
    
    # Ensure we're on the apps page
    if "app/my" not in page.url:
        page.goto(APPS_URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
    
    ss(page, "02_ready")
    
    # === Find and click "新建应用" ===
    print("\n" + "=" * 60)
    print("Step 2: Clicking 新建应用...")
    print("=" * 60)
    
    # First, try to find the exact element and its parent
    clicked = False
    
    # Try approach: find the button by its structure - it's likely a div/span with specific class
    btn_data = page.evaluate("""() => {
        const results = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
        let node;
        while (node = walker.nextNode()) {
            const text = (node.textContent || '').trim();
            if (text === '新建应用' && node.children.length === 0) {
                const rect = node.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    // Get full path
                    let path = [];
                    let parent = node.parentElement;
                    for (let i = 0; i < 5 && parent; i++) {
                        path.push({
                            tag: parent.tagName,
                            cls: (parent.className?.toString() || '').substring(0, 80),
                            id: parent.id || ''
                        });
                        parent = parent.parentElement;
                    }
                    results.push({
                        tag: node.tagName,
                        text: text,
                        x: Math.round(rect.x + rect.width/2),
                        y: Math.round(rect.y + rect.height/2),
                        w: Math.round(rect.width),
                        h: Math.round(rect.height),
                        parentPath: path
                    });
                }
            }
        }
        return results;
    }""")
    
    print(f"Found {len(btn_data)} '新建应用' elements:")
    for b in btn_data:
        print(f"  [{b['tag']}] at ({b['x']},{b['y']}) size={b['w']}x{b['h']}")
        print(f"    Parent chain: {b['parentPath'][:3]}")
    
    if btn_data:
        # Try clicking each one
        for bd in btn_data:
            # Try clicking the parent element
            parent = bd['parentPath'][0]
            parent_cls = parent['cls'].split()[0] if parent['cls'] else ''
            
            if parent_cls:
                try:
                    el = page.locator(f".{parent_cls}").first
                    if el.count() > 0:
                        print(f"  Trying to click .{parent_cls}")
                        el.click()
                        page.wait_for_timeout(4000)
                        clicked = True
                        break
                except:
                    pass
            
            # Try clicking by coordinates
            if not clicked:
                print(f"  Trying coordinate click at ({bd['x']},{bd['y']})")
                page.mouse.click(bd['x'], bd['y'])
                page.wait_for_timeout(4000)
                clicked = True
                break
    
    if not clicked:
        # Fallback to text selectors
        for sel in ["text=新建应用", "span:has-text('新建应用')", "div:has-text('新建应用')"]:
            try:
                el = page.locator(sel).last
                if el.is_visible(timeout=2000):
                    print(f"  Clicking via: {sel}")
                    el.click(force=True)
                    page.wait_for_timeout(4000)
                    clicked = True
                    break
            except:
                continue
    
    if not clicked:
        print("  ERROR: Could not click 新建应用!")
        ss(page, "error_no_click")
        browser.close()
        sys.exit(1)
    
    ss(page, "03_after_click")
    
    # Check if captcha appeared again
    has_captcha2 = page.evaluate("""() => {
        return document.body.innerText.includes('安全验证');
    }""")
    
    if has_captcha2:
        print("\n*** CAPTCHA DETECTED after clicking! ***")
        print("Please solve it again... waiting 30s...")
        for i in range(15):
            time.sleep(2)
            still = page.evaluate("""() => document.body.innerText.includes('安全验证');""")
            if not still:
                print("  Solved!")
                break
            if i % 3 == 0:
                print(f"  ...{i*2}s")
    
    # === Check for dialog/modal ===
    print("\n" + "=" * 60)
    print("Step 3: Checking for dialog...")
    print("=" * 60)
    
    page.wait_for_timeout(2000)
    
    dialog_check = page.evaluate("""() => {
        const result = {modals: [], inputs: []};
        
        // All modals/dialogs
        const containers = document.querySelectorAll('.ant-modal-wrap, .ant-modal, .ant-drawer, [class*=modal], [class*=Modal], [class*=dialog], [class*=Dialog], [class*=drawer], [class*=Drawer], [role=dialog]');
        containers.forEach(c => {
            const rect = c.getBoundingClientRect();
            if (rect.width > 50 && rect.height > 50) {
                result.modals.push({
                    cls: (c.className?.toString() || '').substring(0, 100),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height),
                    visible: c.offsetParent !== null,
                    text: (c.textContent || '').substring(0, 200)
                });
            }
        });
        
        // Visible inputs
        document.querySelectorAll('input:not([type=hidden]), textarea').forEach(inp => {
            if (inp.offsetParent !== null) {
                const rect = inp.getBoundingClientRect();
                if (rect.width > 50) {
                    result.inputs.push({
                        type: inp.type || inp.tagName,
                        placeholder: inp.placeholder || '',
                        name: inp.name || '',
                        id: inp.id || '',
                        cls: (inp.className?.toString() || '').substring(0, 60),
                        w: Math.round(rect.width),
                        h: Math.round(rect.height)
                    });
                }
            }
        });
        
        return result;
    }""")
    
    print(f"  Modals found: {len(dialog_check['modals'])}")
    for m in dialog_check['modals']:
        print(f"    {m['cls'][:60]} | {m['w']}x{m['h']} | vis={m['visible']}")
        print(f"    Text: {m['text'][:100]}")
    
    print(f"  Inputs found: {len(dialog_check['inputs'])}")
    for inp in dialog_check['inputs']:
        print(f"    [{inp['type']}] placeholder='{inp['placeholder']}' name='{inp['name']}' {inp['w']}x{inp['h']}")
    
    ss(page, "04_dialog_check")
    
    # If no dialog, try clicking 新建应用 differently
    if not dialog_check['modals']:
        print("\n  No dialog found! Trying alternative click methods...")
        
        # Try clicking the "新建应用" in the "分组" section
        # The page has two "新建应用" - one is for groups and one is for apps
        # We want the one under "我的应用"
        
        # Get all "新建应用" text nodes with their parents
        alt_btns = page.evaluate("""() => {
            const results = [];
            const all = document.querySelectorAll('*');
            for (const el of all) {
                if (el.children.length === 0 && el.textContent.trim() === '新建应用') {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0) {
                        results.push({
                            x: rect.x + rect.width/2,
                            y: rect.y + rect.height/2,
                            parentCls: el.parentElement?.className || '',
                            parentTag: el.parentElement?.tagName || '',
                            grandparentCls: el.parentElement?.parentElement?.className || ''
                        });
                    }
                }
            }
            return results;
        }""")
        
        print(f"  Found {len(alt_btns)} '新建应用' text nodes:")
        for i, b in enumerate(alt_btns):
            print(f"    [{i}] parent={b['parentTag']}.{b['parentCls'][:40]} grandparent={b['grandparentCls'][:40]} at ({b['x']:.0f},{b['y']:.0f})")
        
        # Click the second one (usually the app creation one, not the group one)
        if len(alt_btns) >= 2:
            print(f"  Clicking the SECOND one at ({alt_btns[1]['x']:.0f},{alt_btns[1]['y']:.0f})")
            page.mouse.click(alt_btns[1]['x'], alt_btns[1]['y'])
        elif len(alt_btns) == 1:
            print(f"  Clicking at ({alt_btns[0]['x']:.0f},{alt_btns[0]['y']:.0f})")
            page.mouse.click(alt_btns[0]['x'], alt_btns[0]['y'])
        
        page.wait_for_timeout(4000)
        ss(page, "04b_alt_click")
        
        # Check again
        dialog_check2 = page.evaluate("""() => {
            const result = [];
            const containers = document.querySelectorAll('.ant-modal-wrap, .ant-modal, [class*=modal], [class*=dialog], [role=dialog]');
            containers.forEach(c => {
                const rect = c.getBoundingClientRect();
                if (rect.width > 50) {
                    result.push({
                        cls: (c.className?.toString() || '').substring(0, 80),
                        w: Math.round(rect.width),
                        h: Math.round(rect.height)
                    });
                }
            });
            return result;
        }""")
        print(f"  Modals after alt click: {len(dialog_check2)}")
        for m in dialog_check2:
            print(f"    {m['cls']} | {m['w']}x{m['h']}")
    
    # === Step 4: Fill app name in dialog ===
    print("\n" + "=" * 60)
    print("Step 4: Filling app name...")
    print("=" * 60)
    
    # Get fresh input list
    inputs = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('input:not([type=hidden])')).filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 50 && el.offsetParent !== null;
        }).map(el => ({
            placeholder: el.placeholder || '',
            name: el.name || '',
            id: el.id || '',
            cls: (el.className?.toString() || '').substring(0, 80)
        }));
    }""")
    
    print(f"  Visible inputs: {len(inputs)}")
    for inp in inputs:
        print(f"    placeholder='{inp['placeholder']}' name='{inp['name']}' id='{inp['id']}'")
    
    filled = False
    for inp in inputs:
        try:
            if inp['placeholder'] and '搜索' in inp['placeholder']:
                continue  # Skip search box
            
            if inp['name']:
                el = page.locator(f"input[name='{inp['name']}']").first
            elif inp['id']:
                el = page.locator(f"#{inp['id']}").first
            else:
                el = page.locator(".ant-modal input:visible").first
            
            if el.count() > 0:
                el.click()
                el.fill("")
                page.wait_for_timeout(300)
                el.fill(APP_NAME)
                page.wait_for_timeout(1000)
                print(f"  Filled: {APP_NAME}")
                filled = True
                break
        except Exception as e:
            print(f"  Failed: {e}")
    
    if not filled:
        print("  WARNING: Could not fill app name!")
    
    ss(page, "05_name_filled")
    
    # === Step 5: Click confirm ===
    print("\n" + "=" * 60)
    print("Step 5: Clicking confirm button...")
    print("=" * 60)
    
    # Get all buttons in any modal/dialog
    all_btns = page.evaluate("""() => {
        const btns = [];
        // Look within modal containers
        const modals = document.querySelectorAll('.ant-modal-wrap, .ant-modal, [class*=modal], [class*=dialog]');
        for (const modal of modals) {
            const rect = modal.getBoundingClientRect();
            if (rect.width > 0) {
                const buttons = modal.querySelectorAll('button, .ant-btn');
                buttons.forEach(b => {
                    const br = b.getBoundingClientRect();
                    if (br.width > 0) {
                        btns.push({
                            text: (b.textContent || '').trim(),
                            cls: (b.className?.toString() || '').substring(0, 60),
                            x: br.x + br.width/2,
                            y: br.y + br.height/2
                        });
                    }
                });
            }
        }
        return btns;
    }""")
    
    print(f"  Buttons in modals: {len(all_btns)}")
    for b in all_btns:
        print(f"    '{b['text']}' cls={b['cls'][:40]}")
    
    confirmed = False
    for b in all_btns:
        if any(kw in b['text'] for kw in ['确定', '创建', '保存', '提交', '确认']):
            try:
                el = page.locator(f"button:has-text('{b['text']}')").first
                if el.is_visible(timeout=1000):
                    print(f"  Clicking: '{b['text']}'")
                    el.click()
                    page.wait_for_timeout(5000)
                    confirmed = True
                    break
            except:
                pass
    
    if not confirmed and all_btns:
        # Click the last button (usually confirm)
        try:
            print(f"  Clicking last button: '{all_btns[-1]['text']}'")
            page.mouse.click(all_btns[-1]['x'], all_btns[-1]['y'])
            page.wait_for_timeout(5000)
            confirmed = True
        except:
            pass
    
    ss(page, "06_after_confirm")
    
    # === Step 6: Verify ===
    print("\n" + "=" * 60)
    print("Step 6: Verifying app creation...")
    print("=" * 60)
    
    page.wait_for_timeout(3000)
    print(f"  Current URL: {page.url}")
    
    # Go back to apps list
    page.goto(APPS_URL, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    
    has_app = page.evaluate("""() => {
        return document.body.innerText.includes('泡泡玛特');
    }""")
    
    print(f"  App '泡泡玛特' found: {has_app}")
    
    if has_app:
        print("\n  *** SUCCESS! App created! ***")
        # Click into the app
        try:
            app_el = page.locator("text=泡泡玛特").first
            if app_el.is_visible(timeout=3000):
                app_el.click()
                page.wait_for_timeout(5000)
                print(f"  Entered app. URL: {page.url}")
        except:
            pass
    else:
        print("\n  App might not have been created. Check screenshots.")
    
    ss(page, "07_final")
    
    # Save session
    context.storage_state(path=SESSION)
    print("Session saved.")
    
    print("\nBrowser will stay open for 10 seconds...")
    time.sleep(10)
    browser.close()
    print("Done!")
