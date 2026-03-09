from playwright.sync_api import sync_playwright

def fetch_calendar_html(url: str = "https://www.forexfactory.com/calendar") -> str:
    print(f"[*] Starting headless browser and navigating to {url}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle", timeout=15000)
            
            html_content = page.content()
            print("[+] Successfully extracted HTML.")
            return html_content
            
        except Exception as e:
            print(f"[-] Error fetching page: {e}")
            return ""
            
        finally:
            browser.close()

if __name__ == "__main__":
    html = fetch_calendar_html()
    if html:
        print(f"[*] Extracted {len(html)} characters of HTML.")
        