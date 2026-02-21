from playwright.sync_api import sync_playwright

def scan_agenda_modern():
    with sync_playwright() as p:
        # Launch browser (headless=False means you can see it working)
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        
        # Go to the site
        page.goto("https://storeycounty.org/AgendaCenter")
        
        # Click the "Planning Commission" filter if it exists (hypothetical)
        # Playwright auto-waits for this to be clickable
        # page.get_by_text("Planning Commission").click()
        
        # Find the first PDF link in the table
        # We look for a link pointing to a PDF inside a specific table row
        # This is robust: it waits for the selector to appear
        try:
            download = page.wait_for_selector("a[href$='.pdf']", timeout=5000)
            url = download.get_attribute("href")
            print(f"Found PDF URL: {url}")
        except:
            print("No PDF found or timed out.")
            
        browser.close()

if __name__ == "__main__":
    scan_agenda_modern()