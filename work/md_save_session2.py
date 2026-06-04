import time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"

print("=" * 60)
print("Opening browser for manual login...")
print("Phone: 18925214672 / Password: q474732204")
print("Solve the captcha in the browser window!")
print("The script will auto-detect when youre logged in.")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="msedge")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    
    page.goto("https://www.mingdao.com/login", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(2000)
    
    # Wait for login by detecting URL change away from login page
    print("\nWaiting for you to log in... (max 10 minutes)")
    print("Fill in phone + password, solve captcha, click login button")
    
    try:
        # Wait until URL changes from login page
        for i in range(300):  # 10 minutes max
            time.sleep(2)
            url = page.url
            if "/login" not in url and "login" not in url.lower():
                print(f"\nDetected login success! URL: {url}")
                break
            if i % 15 == 0 and i > 0:
                print(f"  Still waiting... ({i*2}s elapsed)")
        else:
            print("\nTimeout waiting for login. Saving whatever state we have.")
    except Exception as e:
        print(f"Error during wait: {e}")
    
    # Save session
    page.wait_for_timeout(3000)
    context.storage_state(path=SESSION)
    print(f"\nSession saved to: {SESSION}")
    
    # Navigate to apps page to verify
    page.goto("https://www.mingdao.com/app/my", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(3000)
    
    # Check for captcha on apps page
    has_captcha = page.evaluate("""() => {
        const t = document.body.innerText || '';
        return t.includes('安全验证') || t.includes('拼图');
    }""")
    
    if has_captcha:
        print("\nCaptcha on apps page! Please solve it in browser...")
        for i in range(120):
            time.sleep(2)
            still = page.evaluate("""() => {
                return (document.body.innerText||'').includes('安全验证') || (document.body.innerText||'').includes('拼图');
            }""")
            if not still:
                print("  Captcha solved!")
                break
            if i % 15 == 0 and i > 0:
                print(f"  ...{i*2}s")
    
    # Final save
    context.storage_state(path=SESSION)
    page.screenshot(path=r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict\md_session_ok.png")
    print("Final session saved. Screenshot taken.")
    
    print("\nBrowser will close in 5 seconds...")
    time.sleep(5)
    browser.close()
    print("Done! Session is ready.")
