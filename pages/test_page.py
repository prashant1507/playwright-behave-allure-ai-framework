"""
Test Page Object Model for the main test page.
"""
from .base_page import BasePage

class TestPage(BasePage):
    """Page object for the main test page."""
    
    # Page URL
    URL = ""
    
    # Page elements
    PAGE_TITLE = "h1"
    GET_SECTION = "h2:has-text('GET')"
    POST_SECTION = "h2:has-text('POST')"
    RESPONSE_SECTION = "pre"
    
    def navigate_to_test_page(self, base_url: str):
        """Navigate to the test page."""
        full_url = f"{base_url}/{self.URL}"
        self.navigate_to(full_url)
        self.wait_for_page_load()
    
    def get_page_title(self) -> str:
        """Get the page title."""
        return self.get_element_text(self.PAGE_TITLE)
    
    def get_page_content(self) -> str:
        """Get the page content for verification."""
        return self.get_page_text()
    
    def is_get_section_visible(self) -> bool:
        """Check if the GET section is visible."""
        return self.is_element_visible(self.GET_SECTION)
    
    def is_post_section_visible(self) -> bool:
        """Check if the POST section is visible."""
        return self.is_element_visible(self.POST_SECTION)
    
    def get_response_content(self) -> str:
        """Get the response content."""
        return self.get_element_text(self.RESPONSE_SECTION) 