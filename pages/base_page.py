import playwright.sync_api
from playwright.sync_api import Page
import logging

from utils.logger import log_info_emoji


def ai_selector_healing(context, text):
    locator = ""
    log_info_emoji("⚠️ ", "Selector failed. Healing...")
    new_selector = context.ai.heal_selector(
        original_selector=text,  # The raw text you're searching
        label="Text",  # Semantic label (optional, helps AI)
        context=context
    )

    try:
        locator = context.page.locator(new_selector)
        log_info_emoji("✅ ", "Locator found after healing.")
    except Exception as e:
        log_info_emoji("❌ ", f"Final selector also failed: {e}")
    return locator

class BasePage:

    def __init__(self, page: Page, context):
        self.page = page
        self.context = context
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def navigate_to(self, url: str):
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def wait_for_page_load(self):
        self.page.wait_for_load_state("networkidle")
    
    def get_page_content(self):
        return self.page.content()
    
    def click_element(self, selector: str):
        self.page.click(selector)
    
    def fill_input(self, selector: str, value: str):
        try:
            self.page.locator(selector).wait_for(timeout=5000)
            self.page.fill(selector, value)
        except playwright.sync_api.TimeoutError:
            locator = ai_selector_healing(context=self.context, text=selector)
            locator.fill(value)

    
    def select_option(self, selector: str, value: str):
        self.page.select_option(selector, value)
    
    def check_checkbox(self, selector: str):
        self.page.check(selector)
    
    def uncheck_checkbox(self, selector: str):
        self.page.uncheck(selector)
    
    def is_element_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)
    
    def get_element_text(self, selector: str) -> str:
        return self.page.text_content(selector)
    
    def get_page_text(self) -> str:
        return self.page.content().lower() 