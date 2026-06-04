from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel='msedge')
    context = browser.new_context()
    page = context.new_page()
    
    page.goto('https://www.mingdao.com/login', timeout=30000)
    page.wait_for_timeout(5000)
    print('Page title:', page.title())
    page.screenshot(path='C:/Users/Administrator/Desktop/loading.png')
    
    # Get all input fields with more detail
    inputs = page.query_selector_all('input')
    print(f'Found {len(inputs)} inputs')
    for i, inp in enumerate(inputs):
        try:
            attrs = inp.evaluate('''el => ({
                type: el.type, 
                name: el.name, 
                placeholder: el.placeholder, 
                id: el.id,
                className: el.className,
                parentTag: el.parentElement ? el.parentElement.tagName : null
            })''')
            print(f'  Input {i}: {json.dumps(attrs)}')
        except:
            print(f'  Input {i}: (error reading)')
    
    # Get all buttons
    buttons = page.query_selector_all('button, [role="button"], .btnForLogin')
    print(f'\nFound {len(buttons)} buttons')
    for i, btn in enumerate(buttons):
        try:
            text = btn.inner_text()
            cls = btn.get_attribute('class')
            print(f'  Button {i}: text="{text[:50]}", class="{cls}"')
        except:
            pass
    
    browser.close()
