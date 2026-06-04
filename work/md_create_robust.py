"""Create Pop Mart app in Mingdao - complete robust version"""
import time, os, json, sys
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"
APP_NAME = "泡泡玛特深圳市场分析"

def ss(page, name):
    path = os.path.join(SC, f"md3_{name}.png")
    page.screenshot(path=path)
    print(f"  [SCREENSHOT] {name}")

def dump_buttons(page):
    """Debug: dump all visible buttons"""
    return page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button, [role="button"], .ant-btn, a.btn')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && el.offsetParent !== null;
        }).map(el => ({
            text: (el.textContent || '').trim().substring(0,40),
            tag: el.tagName,
            cls: (el.className?.toString() || '').substring(0,60)
        }));
    }""")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        storage_state=SESSION
    )
    page = context.new_page()
    
    # === STEP 1: Navigate to apps page ===
    print("=" * 60)
    print("STEP 1: Navigating to apps page...")
    page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(4000)
    ss(page, "01_apps_page")
    
    url = page.url
    title = page.title()
    print(f"  URL: {url}")
    print(f"  Title: {title}")
    
    # Check if we got redirected to login
    if "login" in url.lower() or "passport" in url.lower():
        print("  ERROR: Session expired! Need to re-login.")
        print("  Opening login page for manual login...")
        # Clear old session and open login
        page2 = context.new_page()
        page2.goto("https://www.mingdao.com/dashboard", wait_until="domcontentloaded", timeout=15000)
        page2.screenshot(path=os.path.join(SC, "md3_login_needed.png"))
        print("  Please log in manually. Waiting 60s...")
        for i in range(30):
            time.sleep(2)
            if "dashboard" in page2.url or "portal" in page2.url:
                print(f"  Login detected!")
                break
            if i % 5 == 0:
                print(f"    ...{i*2}s")
        context.storage_state(path=SESSION)
        print("  Session saved. Continuing...")
        page2.close()
        # Re-navigate
        page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(4000)
        ss(page, "01b_apps_after_login")
    
    # === STEP 2: Check for existing app ===
    print("\nSTEP 2: Checking for existing app...")
    existing = page.evaluate(f"""() => {{
        const els = document.querySelectorAll('span, a, div, h3, p');
        const results = [];
        for (const el of els) {{
            const t = (el.textContent || '').trim();
            if (t.includes('泡泡玛特') || t.includes('Pop Mart') || t.includes('POPMART')) {{
                results.push({{
                    text: t.substring(0, 50),
                    tag: el.tagName,
                    cls: (el.className?.toString() || '').substring(0, 50)
                }});
            }}
        }}
        return results;
    }}""")
    
    if existing:
        print(f"  Found existing app references: {existing}")
        print("  App may already exist! Proceeding to open it...")
        for item in existing:
            try:
                el = page.locator(f"text={item['text'][:20]}").first
                if el.is_visible(timeout=2000):
                    el.click()
                    page.wait_for_timeout(4000)
                    print(f"  Clicked on existing app!")
                    break
            except:
                continue
    else:
        print("  No existing app found. Will create new one.")
    
    # === STEP 3: Click "新建应用" ===
    print("\nSTEP 3: Clicking 新建应用...")
    clicked = False
    
    # Approach 1: text selector
    for sel in ["text=新建应用", "span:has-text('新建应用')"]:
        try:
            el = page.locator(sel).last
            if el.is_visible(timeout=2000):
                print(f"  Found via: {sel}")
                el.click(force=True)
                page.wait_for_timeout(3500)
                clicked = True
                break
        except Exception as e:
            print(f"  Failed {sel}: {e}")
    
    if not clicked:
        # Approach 2: Find by text content
        btn_data = page.evaluate("""() => {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
            const results = [];
            let node;
            while (node = walker.nextNode()) {
                const text = (node.textContent || '').trim();
                if (text === '新建应用' && node.children.length === 0) {
                    const rect = node.getBoundingClientRect();
                    results.push({
                        tag: node.tagName,
                        text: text,
                        x: rect.x + rect.width/2,
                        y: rect.y + rect.height/2,
                        parentTag: node.parentElement?.tagName || '',
                        parentCls: (node.parentElement?.className?.toString() || '').substring(0, 80)
                    });
                }
            }
            return results;
        }""")
        print(f"  Button search results: {btn_data}")
        
        if btn_data:
            for bd in btn_data:
                print(f"  Clicking at ({bd['x']:.0f}, {bd['y']:.0f}) via parent class")
                try:
                    parent = page.locator(f".{bd['parentCls'].split()[0]}")
                    if parent.count() > 0:
                        parent.first.click()
                        page.wait_for_timeout(3500)
                        clicked = True
                        break
                except:
                    pass
            
            if not clicked:
                # Click by coordinates
                page.mouse.click(btn_data[0]['x'], btn_data[0]['y'])
                page.wait_for_timeout(3500)
                clicked = True
    
    if not clicked:
        print("  ERROR: Could not find 新建应用 button!")
        # Dump page for debugging
        body_text = page.evaluate("() => document.body.innerText.substring(0, 500)")
        print(f"  Body text: {body_text[:200]}")
        browser.close()
        sys.exit(1)
    
    ss(page, "02_after_create_click")
    
    # === STEP 4: Handle the dialog ===
    print("\nSTEP 4: Handling dialog...")
    
    # Check what appeared
    dialog_check = page.evaluate("""() => {
        const result = {modals: [], drawers: [], inputs: []};
        
        // Check modals
        const modals = document.querySelectorAll('.ant-modal, [class*=modal], [class*=Modal], [class*=dialog], [class*=Dialog]');
        modals.forEach(m => {
            const rect = m.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                result.modals.push({
                    cls: (m.className?.toString() || '').substring(0, 80),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height),
                    text: (m.textContent || '').substring(0, 100)
                });
            }
        });
        
        // Check drawers
        const drawers = document.querySelectorAll('.ant-drawer, [class*=drawer], [class*=Drawer]');
        drawers.forEach(d => {
            const rect = d.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                result.drawers.push({
                    cls: (d.className?.toString() || '').substring(0, 80),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height)
                });
            }
        });
        
        // Check visible inputs
        const inputs = document.querySelectorAll('input:not([type=hidden]), textarea');
        inputs.forEach(inp => {
            if (inp.offsetParent !== null) {
                result.inputs.push({
                    type: inp.type || inp.tagName,
                    placeholder: inp.placeholder || '',
                    name: inp.name || '',
                    id: inp.id || '',
                    cls: (inp.className?.toString() || '').substring(0, 60)
                });
            }
        });
        
        return result;
    }""")
    
    print(f"  Modals: {dialog_check['modals']}")
    print(f"  Drawers: {dialog_check['drawers']}")
    print(f"  Visible inputs: {dialog_check['inputs']}")
    
    # === STEP 5: Fill app name ===
    print(f"\nSTEP 5: Filling app name: {APP_NAME}")
    
    if dialog_check['inputs']:
        # Try each visible input
        filled = False
        for inp_info in dialog_check['inputs']:
            try:
                if inp_info['name']:
                    el = page.locator(f"input[name='{inp_info['name']}']")
                elif inp_info['id']:
                    el = page.locator(f"#{inp_info['id']}")
                elif inp_info['placeholder']:
                    el = page.locator(f"input[placeholder='{inp_info['placeholder']}']")
                else:
                    el = page.locator(".ant-modal input:visible").first
                
                if el.count() > 0 and el.first.is_visible(timeout=2000):
                    el.first.click()
                    el.first.fill("")
                    page.wait_for_timeout(500)
                    el.first.fill(APP_NAME)
                    page.wait_for_timeout(1000)
                    print(f"  Filled via: name={inp_info['name']}, id={inp_info['id']}")
                    filled = True
                    break
            except Exception as e:
                print(f"  Try failed: {e}")
                continue
        
        if not filled:
            # Last resort: first visible input in modal
            try:
                modal_input = page.locator(".ant-modal-wrap input:visible, [class*=modal] input:visible").first
                if modal_input.is_visible(timeout=2000):
                    modal_input.click()
                    modal_input.fill("")
                    modal_input.fill(APP_NAME)
                    page.wait_for_timeout(1000)
                    print("  Filled via modal input fallback")
                    filled = True
            except Exception as e:
                print(f"  Fallback fill failed: {e}")
    
    ss(page, "03_name_filled")
    
    # === STEP 6: Find and click confirm button ===
    print("\nSTEP 6: Finding confirm button...")
    
    # Dump ALL buttons first
    all_btns = dump_buttons(page)
    print(f"  All visible buttons ({len(all_btns)}):")
    for b in all_btns:
        print(f"    [{b['tag']}] '{b['text']}' cls={b['cls'][:50]}")
    
    # Try each confirm-like button
    confirm_keywords = ['确定', '创建', '保存', '提交', '确认', 'OK', 'Create', 'Save', 'Submit']
    confirmed = False
    
    for kw in confirm_keywords:
        for btn in all_btns:
            if kw in btn['text']:
                try:
                    el = page.locator(f"button:has-text('{btn['text']}')").first
                    if el.is_visible(timeout=1000):
                        print(f"  Clicking: '{btn['text']}'")
                        el.click()
                        page.wait_for_timeout(5000)
                        confirmed = True
                        break
                except Exception as e:
                    print(f"  Failed button click '{btn['text']}': {e}")
        if confirmed:
            break
    
    # If keyword match failed, try ant-btn-primary
    if not confirmed:
        try:
            primary_btn = page.locator(".ant-btn-primary:visible").first
            if primary_btn.is_visible(timeout=1000):
                txt = primary_btn.text_content() or ''
                print(f"  Clicking .ant-btn-primary: '{txt[:30]}'")
                primary_btn.click()
                page.wait_for_timeout(5000)
                confirmed = True
        except Exception as e:
            print(f"  Primary button failed: {e}")
    
    # If still not confirmed, click the last button in modal (usually confirm)
    if not confirmed:
        try:
            last_btn = page.locator(".ant-modal-footer button:last-child, .ant-modal button:last-of-type").first
            if last_btn.is_visible(timeout=1000):
                txt = last_btn.text_content() or ''
                print(f"  Clicking last modal button: '{txt[:30]}'")
                last_btn.click()
                page.wait_for_timeout(5000)
                confirmed = True
        except Exception as e:
            print(f"  Last button failed: {e}")
    
    ss(page, "04_after_confirm")
    
    # === STEP 7: Wait and verify ===
    print(f"\nSTEP 7: Verifying...")
    page.wait_for_timeout(5000)
    current_url = page.url
    print(f"  Current URL: {current_url}")
    
    # Navigate back to apps page to check
    page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(4000)
    
    # Check for the app
    app_check = page.evaluate(f"""() => {{
        const all = document.body.innerText;
        return {{
            hasApp: all.includes('泡泡玛特'),
            sample: all.substring(0, 300)
        }};
    }}""")
    
    print(f"  App exists: {app_check['hasApp']}")
    print(f"  Page sample: {app_check['sample'][:200]}")
    
    if app_check['hasApp']:
        print("\n  SUCCESS! App '泡泡玛特深圳市场分析' has been created!")
        # Click into the app
        try:
            app_link = page.locator("text=泡泡玛特").first
            if app_link.is_visible(timeout=3000):
                app_link.click()
                page.wait_for_timeout(5000)
                print(f"  Clicked into app. URL: {page.url}")
        except Exception as e:
            print(f"  Could not click into app: {e}")
    else:
        print("\n  WARNING: App may not have been created. Check the dialog behavior.")
        # Dump full page text for debugging
        full_text = page.evaluate("() => document.body.innerText")
        print(f"  Full page text:\n{full_text[:1000]}")
    
    ss(page, "05_verification")
    
    # Save the session (cookies might have been updated)
    context.storage_state(path=SESSION)
    print(f"\nSession saved.")
    
    page.wait_for_timeout(3000)
    browser.close()
    print("\nDone!")
