import time, os
from playwright.sync_api import sync_playwright

SESSION = r"C:\Users\Administrator\Desktop\mingdao_session.json"

print("=" * 60)
print("Step 1: Open browser for manual login")
print("=" * 60)
print("\nA browser window will open shortly.")
print("Please log into Mingdao (https://www.mingdao.com/login)")
print("Phone: 18925214672")
print("Password: q474732204")
print("\nIMPORTANT: Solve the slider captcha after login!")
print("After you see the main dashboard, press Enter in THIS terminal.\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="msedge")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://www.mingdao.com/login", wait_until="domcontentloaded", timeout=15000)
    
    input("\n>>> Press Enter after you have logged in and see the dashboard <<<")
    
    # Save session
    context.storage_state(path=SESSION)
    print(f"\nSession saved to: {SESSION}")
    print("You can close the browser now.")
    browser.close()
    print("Done! Now run the full build script.")
