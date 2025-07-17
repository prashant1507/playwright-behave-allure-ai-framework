from playwright.sync_api import sync_playwright

class BrowserManager:
    def __init__(self, browser_type="chromium", headless=False):
        self.playwright = None
        self.browser = None
        self.page = None
        self.headless = headless
        self.browser_type = browser_type

    def start(self):
        self.playwright = sync_playwright().start()
        browser_launcher = getattr(self.playwright, self.browser_type)
        self.browser = browser_launcher.launch(headless=self.headless)
        self.page = self.browser.new_page()
        return self.page

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop() 