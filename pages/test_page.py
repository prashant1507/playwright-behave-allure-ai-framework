from .base_page import BasePage

class TestPage(BasePage):
    # Page URL
    URL = ""
    
    def navigate_to_test_page(self, base_url: str):
        full_url = f"{base_url}/{self.URL}"
        self.navigate_to(full_url)
        self.wait_for_page_load()
    
    def get_page_content(self) -> str:
        return self.get_page_text()