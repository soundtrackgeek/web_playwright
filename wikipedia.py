from playwright.sync_api import sync_playwright
import datetime
import os

def scrape_random_wikipedia():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Go to random Wikipedia page
        page.goto('https://en.wikipedia.org/wiki/Special:Random')
        page.wait_for_load_state('networkidle')
        
        # Extract data
        title = page.locator('h1#firstHeading').text_content()
        
        # Get first paragraph (introduction)
        first_para = page.locator('div.mw-parser-output > p:not(.mw-empty-elt)').first.text_content()
        
        # Get URL of the page
        url = page.url
        
        # Get references count
        references = len(page.locator('ol.references li').all())
        
        browser.close()
        
        return {
            'title': title,
            'intro': first_para,
            'url': url,
            'references': references
        }

def save_to_file(data):
    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'wikipedia_article_{timestamp}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Title: {data['title']}\n\n")
        f.write(f"URL: {data['url']}\n\n")
        f.write(f"Introduction:\n{data['intro']}\n\n")
        f.write(f"Number of References: {data['references']}\n")

def main():
    try:
        print("Fetching random Wikipedia article...")
        data = scrape_random_wikipedia()
        save_to_file(data)
        print("Article data has been saved successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()