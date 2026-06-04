from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge')
    context = browser.new_context()
    page = context.new_page()
    
    page.goto('https://www.mingdao.com/login', timeout=30000)
    page.wait_for_timeout(3000)
    print('Page title:', page.title())
    
    try:
        page.wait_for_selector('input', timeout=10000)
        inputs = page.query_selector_all('input')
        print(f'Found {len(inputs)} inputs')
        for i, inp in enumerate(inputs):
            attrs = inp.evaluate('el => ({type: el.type, name: el.name, placeholder: el.placeholder})')
            print(f'  Input {i}: {attrs}')
        
        phone_input = page.query_selector('input[type="text"]')
        if not phone_input:
            all_text_inputs = page.query_selector_all('input:not([type="password"])')
            for inp in all_text_inputs:
                inp_type = inp.get_attribute('type')
                if inp_type != 'password' and inp_type != 'submit' and inp_type != 'checkbox':
                    phone_input = inp
                    break
        if phone_input:
            phone_input.fill('18925214672')
            print('Filled phone')
        
        pwd_input = page.query_selector('input[type="password"]')
        if pwd_input:
            pwd_input.fill('q474732204')
            print('Filled password')
        
        page.wait_for_timeout(1000)
        page.screenshot(path='C:/Users/Administrator/Desktop/pre_login.png')
        print('Pre-login screenshot saved')
        
        login_btn = page.query_selector('button, .btnForLogin, [type="submit"], .Hand')
        if login_btn:
            login_btn.click()
            print('Clicked login button')
            
        page.wait_for_timeout(8000)
        page.screenshot(path='C:/Users/Administrator/Desktop/post_login.png')
        print('Post-login screenshot saved')
        print('Current URL:', page.url)
        print('Page title:', page.title())
        
        cookies = context.cookies()
        with open('C:/Users/Administrator/Desktop/mingdao_cookies.json', 'w') as f:
            json.dump(cookies, f)
        print(f'Saved {len(cookies)} cookies')
        
    except Exception as e:
        print(f'Error: {e}')
        page.screenshot(path='C:/Users/Administrator/Desktop/error_login.png')
    
    browser.close()
