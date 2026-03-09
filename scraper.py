from playwright.sync_api import sync_playwright
from parser import parse_calendar_html
import os
def fetch_calendar_html(url: str = "https://www.forexfactory.com/calendar?week=this") -> str:
    print(f"[*] Starting headless browser and navigating to {url}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            viewport={'width': 1920, 'height': 5000},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle", timeout=15000)

            print("[*] Scrolling to the bottom to load the full week...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            page.wait_for_timeout(2000) 
            
            html_content = page.content()
            print("[+] Successfully extracted HTML.")
            return html_content
            
        except Exception as e:
            print(f"[-] Error fetching page: {e}")
            return ""
            
        finally:
            browser.close()

if __name__ == "__main__":
    page_source = fetch_calendar_html()
    if page_source:
        df = parse_calendar_html(page_source)
        
        print("\n--- Extracted Economic Calendar ---")
        print(df.head(15).to_string())
        os.makedirs("csv result/", exist_ok=True)
        df.to_csv("csv result/forex_calendar.csv", index=False)
        print("\nData saved to forex_calendar.csv")
        