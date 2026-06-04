"""Open Mingdao login page for manual login, then create app"""
import time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"
LOGIN_URL = "https://www.mingdao.com/dashboard"
SCREENSHOTS = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict"

with sync_playwright() as p:
    # Try with saved session first
    print("Attempting with saved session...")
    browser = p.chromium.launch(headless=False)
    
    try:
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            storage_state=SESSION
        )
        page = context.new_page()
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(3000)
        
        # Check if we're logged in or on login page
        title = page.title()
        url = page.url
        print(f"Title: {title}")
        print(f"URL: {url}")
        
        # Check for login page indicators
        has_password = page.locator("input[type=password]").count()
        has_phone = page.locator("input[type=tel], input[placeholder*=手机], input[placeholder*=phone]").count()
        print(f"Password inputs: {has_password}, Phone inputs: {has_phone}")
        
        if has_password > 0 and "login" in url.lower():
            print("Session expired - need fresh login")
            browser.close()
            
            # Open fresh browser for manual login
            print("\nOpening fresh browser for manual login...")
            browser2 = p.chromium.launch(headless=False)
            page2 = browser2.new_page()
            page2.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=15000)
            
            # Take screenshot of login page
            page2.screenshot(path=os.path.join(SCREENSHOTS, "md_fresh_login.png"))
            print("Login page opened. Waiting 60s for manual login...")
            print("Please log in manually in the opened browser window.")
            
            # Wait for login (check every 2 seconds, max 120s)
            for i in range(60):
                time.sleep(2)
                url2 = page2.url
                if "dashboard" in url2 or "portal" in url2:
                    print(f"Login detected! Current URL: {url2}")
                    break
                if i % 5 == 0:
                    print(f"  Waiting... ({i*2}s)")
            
            # Save session
            context2 = page2.context
            context2.storage_state(path=SESSION)
            print(f"Session saved to {SESSION}")
            
            # Now we're logged in - navigate to apps
            page2.screenshot(path=os.path.join(SCREENSHOTS, "md_logged_in.png"))
            
            # Keep browser open for inspection
            print("\nBrowser will stay open for 30s for inspection...")
            time.sleep(30)
            browser2.close()
        else:
            print("Session is VALID - already logged in!")
            page.screenshot(path=os.path.join(SCREENSHOTS, "md_session_valid.png"))
            time.sleep(5)
            browser.close()
            
    except Exception as e:
        print(f"Error: {e}")
        browser.close()
