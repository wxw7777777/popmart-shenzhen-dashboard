from playwright.sync_api import sync_playwright
import json, time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge')
    context = browser.new_context()
    page = context.new_page()
    
    page.goto('https://www.mingdao.com/login', timeout=30000)
    page.wait_for_timeout(3000)
    print('Page loaded:', page.title())
    
    # Fill phone number - use the input with id="txtMobilePhone"
    phone = page.query_selector('#txtMobilePhone')
    if phone:
        phone.click()
        phone.fill('18925214672')
        print('Filled phone: 18925214672')
    else:
        print('Phone input not found')
    
    # Fill password
    pwd = page.query_selector('input[type="password"]')
    if pwd:
        pwd.click()
        pwd.fill('q474732204')
        print('Filled password')
    else:
        print('Password input not found')
    
    page.wait_for_timeout(500)
    
    # Screenshot before clicking login
    page.screenshot(path='C:/Users/Administrator/Desktop/pre_login.png')
    print('Pre-login screenshot saved')
    
    # Click login button
    login_btn = page.query_selector('.btnForLogin')
    if login_btn:
        login_btn.click()
        print('Clicked login')
    else:
        print('Login button not found')
    
    # Wait for navigation/response
    page.wait_for_timeout(8000)
    
    page.screenshot(path='C:/Users/Administrator/Desktop/post_login.png')
    print('Post-login screenshot saved')
    print('Current URL:', page.url)
    print('Page title:', page.title())
    
    # Check for error messages
    try:
        error_texts = page.evaluate('''() => {
            const errors = document.querySelectorAll('[class*="error"], [class*="warn"], .tip, .alert');
            return Array.from(errors).map(e => e.innerText).join(' | ');
        }''')
        if error_texts:
            print('Messages:', error_texts)
    except:
        pass
    
    # Save cookies
    cookies = context.cookies()
    with open('C:/Users/Administrator/Desktop/mingdao_cookies.json', 'w') as f:
        json.dump(cookies, f)
    print(f'Saved {len(cookies)} cookies')
    
    # Save storage state
    context.storage_state(path='C:/Users/Administrator/Desktop/mingdao_session.json')
    print('Saved session state')
    
    browser.close()
