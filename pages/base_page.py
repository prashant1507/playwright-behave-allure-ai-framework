"""
Base Page Object Model class with common functionality.
"""
from playwright.sync_api import Page
import logging

class BasePage:
    """Base page class with common methods for all page objects."""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def navigate_to(self, url: str):
        """Navigate to a specific URL."""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def wait_for_page_load(self):
        """Wait for the page to load completely."""
        self.page.wait_for_load_state("networkidle")
    
    def get_page_content(self):
        """Get the page content."""
        return self.page.content()
    
    def take_screenshot(self, name: str = None):
        """Take a screenshot of the current page."""
        if name is None:
            name = f"screenshot_{self.__class__.__name__.lower()}"
        self.page.screenshot(path=f"reports/screenshots/{name}.png")
        self.logger.info(f"Screenshot saved: {name}.png")
    
    def wait_for_element(self, selector: str, timeout: int = 5000):
        """Wait for an element to be visible."""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def click_element(self, selector: str):
        """Click an element."""
        self.page.click(selector)
    
    def fill_input(self, selector: str, value: str):
        """Fill an input field."""
        self.page.fill(selector, value)
    
    def select_option(self, selector: str, value: str):
        """Select an option from a dropdown."""
        self.page.select_option(selector, value)
    
    def check_checkbox(self, selector: str):
        """Check a checkbox."""
        self.page.check(selector)
    
    def uncheck_checkbox(self, selector: str):
        """Uncheck a checkbox."""
        self.page.uncheck(selector)
    
    def is_element_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.is_visible(selector)
    
    def get_element_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.text_content(selector)
    
    def get_page_text(self) -> str:
        """Get the page text content."""
        return self.page.content().lower() 