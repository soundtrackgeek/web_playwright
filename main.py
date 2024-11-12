from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Basic navigation
        page.goto('https://github.com')
        print("Title:", page.title())
        
        # Screenshots
        page.screenshot(path="github.png")
        
        # Fill forms
        page.goto('https://github.com/login')
        page.fill('input[name="login"]', 'test@example.com')
        page.fill('input[name="password"]', 'password123')
        
        # Multiple tabs
        page2 = browser.new_page()
        page2.goto('https://playwright.dev')
        
        # Network interception
        def handle_route(route):
            if route.request.resource_type == "image":
                route.abort()
            else:
                route.continue_()
                
        page.route("**/*", handle_route)
        
        # Wait for elements
        page.wait_for_selector('input[name="login"]')
        
        # Extract data
        elements = page.query_selector_all('.main-content h1')
        for element in elements:
            print(element.inner_text())
            
        time.sleep(2)  # Keep browser open to see results
        browser.close()

if __name__ == '__main__':
    run()