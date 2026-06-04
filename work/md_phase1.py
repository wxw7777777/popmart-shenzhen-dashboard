import time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
SC = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"
APP_NAME = "泡泡玛特深圳市场分析"

def ss(page, name):
    page.screenshot(path=os.path.join(SC, f"md_{name}.png"))
    print(f"  [SCREENSHOT] {name}")

def captcha_wait(page, label=""):
    """Wait for captcha to be solved by user. Polls every 2s."""
    js = """() => { const t = document.body.innerText || ''; return t.includes('安全验证') || t.includes('拼图') || t.includes('拖动滑块'); }"""
    has = page.evaluate(js)
    if not has:
        return False
    print(f"\n*** 验证码出现 ({label}) - 请在浏览器窗口完成滑块验证 ***")
    print("  脚本每2秒检测一次，验证通过后自动继续...")
    for i in range(300):  # 10 min max
        time.sleep(2)
        still = page.evaluate(js)
        if not still:
            print("  验证码通过！继续执行...")
            page.wait_for_timeout(2000)
            return True
        if i % 30 == 0 and i > 0:
            print(f"  等待中... {i*2}秒 (请在浏览器滑一下验证码)")
    raise TimeoutError("Captcha not solved in 10 minutes")

print("=" * 60)
print("泡泡玛特深圳市场分析 - 明道云自动化构建")
print("=" * 60)
print("\n提示: 遇到验证码时请在浏览器窗口滑动完成，脚本会自动继续。\n")

with sync_playwright() as p:
    # ---- PHASE 1: LOGIN ----
    print("[阶段1] 打开登录页面...")
    browser = p.chromium.launch(headless=False, channel="msedge")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    
    # Try existing session first
    if os.path.exists(SESSION):
        try:
            new_ctx = browser.new_context(viewport={"width": 1440, "height": 900}, storage_state=SESSION)
            page = new_ctx.new_page()
            page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000)
            captcha_wait(page, "apps")
            if "/app/my" in page.url and "login" not in page.url.lower():
                print("  Session valid, already logged in!")
                context = new_ctx
            else:
                page.close()
                new_ctx.close()
                raise Exception("Session expired")
        except:
            print("  Session expired, need fresh login...")
            page = context.new_page()
            page.goto("https://www.mingdao.com/login", wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(2000)
            print("\n  >>> 请在浏览器输入手机号 18925214672 密码 q474732204 并完成验证码 <<<")
            print("  >>> 登入后脚本会自动检测并继续... <<<\n")
            for i in range(300):
                time.sleep(2)
                url = page.url
                if "/login" not in url and "login" not in url.lower():
                    print(f"  检测到登录成功! URL: {url[:60]}")
                    break
                if i % 30 == 0 and i > 0:
                    print(f"  等待登录... ({i*2}秒)")
            else:
                print("  登录超时，请重试")
                browser.close()
                exit(1)
    else:
        page.goto("https://www.mingdao.com/login", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(2000)
        print("\n  >>> 请在浏览器输入手机号 18925214672 密码 q474732204 并完成验证码 <<<")
        print("  >>> 登入后脚本会自动检测并继续... <<<\n")
        for i in range(300):
            time.sleep(2)
            url = page.url
            if "/login" not in url and "login" not in url.lower():
                print(f"  检测到登录成功! URL: {url[:60]}")
                break
            if i % 30 == 0 and i > 0:
                print(f"  等待登录... ({i*2}秒)")
        else:
            print("  登录超时")
            browser.close()
            exit(1)
    
    # Save session after login
    context.storage_state(path=SESSION)
    print("  Session已保存")
    
    # ---- PHASE 2: NAVIGATE TO APPS ----
    print("\n[阶段2] 进入应用列表...")
    page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(4000)
    captcha_wait(page, "应用列表")
    ss(page, "s2_apps")
    print(f"  URL: {page.url[:80]}")
    
    # ---- PHASE 3: FIND OR CREATE APP ----
    print("\n[阶段3] 检查泡泡玛特应用...")
    app_found = page.evaluate("""() => (document.body.innerText||'').includes('泡泡玛特')""")
    print(f"  应用存在: {app_found}")
    
    if not app_found:
        print("  创建新应用中...")
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
        
        if len(btns) >= 2:
            page.mouse.click(btns[1]["x"], btns[1]["y"])
        elif btns:
            page.mouse.click(btns[0]["x"], btns[0]["y"])
        else:
            try:
                page.locator("text=新建应用").last.click()
            except:
                pass
        
        page.wait_for_timeout(4000)
        captcha_wait(page, "创建弹窗")
        ss(page, "s3_dialog")
        
        # Fill app name
        print("  填写应用名称...")
        try:
            inp = page.locator("input:visible").first
            inp.click()
            page.wait_for_timeout(300)
            inp.fill("")
            page.wait_for_timeout(200)
            inp.fill(APP_NAME)
            print(f"  已填写: {APP_NAME}")
        except:
            print("  自动填写失败，请手动输入 '泡泡玛特深圳市场分析' 后按回车键风格的等待...")
            # Try to find any visible input
            for i in range(60):
                time.sleep(2)
                try:
                    txt = page.evaluate("""() => {
                        const inputs = document.querySelectorAll('input:visible');
                        for (const inp of inputs) {
                            if (inp.value && inp.value.includes('泡泡玛特')) return inp.value;
                        }
                        return '';
                    }""")
                    if txt:
                        print(f"  检测到已输入: {txt}")
                        break
                except:
                    pass
                if i % 10 == 0 and i > 0:
                    print(f"  等待手动输入... ({i*2}秒)")
        
        ss(page, "s3_filled")
        
        # Click confirm
        print("  点击确认按钮...")
        try:
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)
        except:
            pass
        
        # Check if dialog still open
        dialog_open = page.evaluate("""() => {
            const modals = document.querySelectorAll('.ant-modal-wrap, .ant-modal, [class*=modal], [role=dialog]');
            for (const m of modals) { const r = m.getBoundingClientRect(); if (r.width > 50 && r.height > 50) return true; }
            return false;
        }""")
        
        if dialog_open:
            btn_info = page.evaluate("""() => {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    const t = (b.textContent||'').trim();
                    if (['确定','创建','保存','OK','确认','提交'].some(k => t.includes(k))) {
                        const r = b.getBoundingClientRect();
                        return {text: t, x: r.x+r.width/2, y: r.y+r.height/2};
                    }
                }
                return null;
            }""")
            if btn_info:
                print(f"  点击 '{btn_info['text']}'")
                page.mouse.click(btn_info["x"], btn_info["y"])
        
        page.wait_for_timeout(5000)
        captcha_wait(page, "创建后")
    
    # ---- PHASE 4: ENTER APP ----
    print("\n[阶段4] 进入应用...")
    if "app/my" not in page.url and "app/" not in page.url.split("/")[-2]:
        page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        captcha_wait(page, "重新进入应用列表")
    
    ss(page, "s4_before_enter")
    
    try:
        app_link = page.locator("text=泡泡玛特").first
        app_link.click(timeout=5000)
        page.wait_for_timeout(5000)
        print(f"  已进入: {page.url[:80]}")
    except:
        print("  自动点击失败。请在浏览器手动点击'泡泡玛特深圳市场分析'应用。")
        print("  等待60秒让你操作...")
        for i in range(30):
            time.sleep(2)
            if "app/" in page.url and "my" not in page.url:
                print("  检测到已进入应用!")
                break
            if i % 10 == 0 and i > 0:
                print(f"  ...{i*2}秒")
    
    captcha_wait(page, "应用内部")
    ss(page, "s4_inside")
    
    # Save session
    context.storage_state(path=SESSION)
    
    # ---- PHASE 5: CHECK STATE ----
    print("\n[阶段5] 检查应用内容...")
    state = page.evaluate("""() => {
        const body = document.body.innerText || '';
        return {
            store: body.includes('门店数据'),
            staff: body.includes('人员开支'),
            product: body.includes('商品销售'),
            revenue: body.includes('应收明细'),
            dashboard: body.includes('驾驶舱') || body.includes('仪表盘'),
            url: window.location.href,
            text: body.substring(0, 500)
        };
    }""")
    
    for k, v in state.items():
        if k != 'text': print(f"  {k}: {v}")
    print(f"  页面片段: {state['text'][:300]}")
    
    missing = []
    if not state['store']: missing.append('门店数据')
    if not state['staff']: missing.append('人员开支')
    if not state['product']: missing.append('商品销售')
    if not state['revenue']: missing.append('应收明细')
    
    ss(page, "s5_state")
    
    if missing:
        print(f"\n  缺少的工作表: {missing}")
        print("\n  >>> 现在需要创建这些工作表。请在浏览器中操作或让脚本尝试自动化 <<<")
        
        # Try to find "新建工作表" button
        create_btns = page.evaluate("""() => {
            const r = [];
            const all = document.querySelectorAll('*');
            for (const el of all) {
                const t = (el.textContent||'').trim();
                if (['新建工作表','新建','+ 新建','添加工作表','创建表','新建表格'].some(k => t.includes(k))) {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) r.push({text: t, x: rect.x+rect.width/2, y: rect.y+rect.height/2});
                }
            }
            return r;
        }""")
        
        print(f"  找到 {len(create_btns)} 个新建按钮:")
        for cb in create_btns:
            print(f"    '{cb['text']}' at ({cb['x']:.0f}, {cb['y']:.0f})")
    
    # ========================================
    # PHASE 6: SAVE FINAL STATE & WAIT
    # ========================================
    context.storage_state(path=SESSION)
    print("\n" + "=" * 60)
    print("脚本暂停于此。浏览器保持打开。")
    print("请查看截图了解当前状态。")
    print("如需继续，请回复告知下一步操作。")
    print("=" * 60)
    
    # Keep browser open
    try:
        time.sleep(600)
    except KeyboardInterrupt:
        pass
    
    browser.close()
    print("完成。")
