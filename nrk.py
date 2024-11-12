from playwright.sync_api import sync_playwright
from datetime import datetime
import os

def scrape_nrk_headlines():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Go to NRK
        page.goto('https://www.nrk.no/')
        
        # Wait for content to load and get headlines
        headlines = page.query_selector_all('h2, h3')
        headline_texts = [h.text_content().strip() for h in headlines if h.text_content().strip()]
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'nrk_headlines_{timestamp}.txt'
        
        # Write headlines to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"NRK Headlines - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for i, headline in enumerate(headline_texts, 1):
                f.write(f"{i}. {headline}\n")
        
        # Close browser
        browser.close()
        
        print(f"Headlines saved to {filename}")

if __name__ == "__main__":
    scrape_nrk_headlines()