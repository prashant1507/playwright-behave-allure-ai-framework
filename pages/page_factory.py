"""
Page Factory for managing page objects.
"""
from .test_page import TestPage
from .contact_form_page import ContactFormPage

class PageFactory:
    """Factory class for creating page objects."""
    
    @staticmethod
    def get_test_page(page):
        """Get TestPage instance."""
        return TestPage(page)
    
    @staticmethod
    def get_contact_form_page(page):
        """Get ContactFormPage instance."""
        return ContactFormPage(page)
    
    @staticmethod
    def get_page(page_name: str, page):
        """Get page object by name."""
        page_map = {
            'test': TestPage,
            'contact_form': ContactFormPage
        }
        
        if page_name not in page_map:
            raise ValueError(f"Unknown page: {page_name}")
        
        return page_map[page_name](page) 