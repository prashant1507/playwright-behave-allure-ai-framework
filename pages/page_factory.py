from .contact_form_page import ContactFormPage
from .test_page import TestPage


class PageFactory:
    
    @staticmethod
    def get_test_page(context):
        return TestPage(context.page, context)
    
    @staticmethod
    def get_contact_form_page(context):
        return ContactFormPage(context.page, context)
    
    @staticmethod
    def get_page(page_name: str, context):
        page_map = {
            'test': TestPage,
            'contact_form': ContactFormPage
        }
        
        if page_name not in page_map:
            raise ValueError(f"Unknown page: {page_name}")
        
        return page_map[page_name](context.page, context)