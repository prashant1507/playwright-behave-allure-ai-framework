"""
Contact Form Page Object Model.
"""
from .base_page import BasePage

class ContactFormPage(BasePage):
    """Page object for the contact form page."""
    
    # Page URL
    URL = "forms/post"
    
    # Form elements
    CUSTOMER_NAME_INPUT = 'input[name="custname"]'
    CUSTOMER_PHONE_INPUT = 'input[name="custtel"]'
    CUSTOMER_EMAIL_INPUT = 'input[name="custemail"]'
    PIZZA_SIZE_SELECT = 'select[name="size"]'
    TOPPING_CHECKBOX = 'input[name="topping"]'
    COMMENTS_TEXTAREA = 'textarea[name="comments"]'
    SUBMIT_BUTTON = 'input[type="submit"]'
    
    def navigate_to_contact_form(self, base_url: str):
        """Navigate to the contact form page."""
        full_url = f"{base_url}/{self.URL}"
        self.navigate_to(full_url)
        self.wait_for_page_load()
    
    def fill_customer_name(self, name: str):
        """Fill the customer name field."""
        self.fill_input(self.CUSTOMER_NAME_INPUT, name)
    
    def fill_customer_phone(self, phone: str):
        """Fill the customer phone field."""
        self.fill_input(self.CUSTOMER_PHONE_INPUT, phone)
    
    def fill_customer_email(self, email: str):
        """Fill the customer email field."""
        self.fill_input(self.CUSTOMER_EMAIL_INPUT, email)
    
    def select_pizza_size(self, size: str):
        """Select pizza size from dropdown."""
        self.select_option(self.PIZZA_SIZE_SELECT, size)
    
    def check_topping(self):
        """Check the topping checkbox."""
        self.check_checkbox(self.TOPPING_CHECKBOX)
    
    def uncheck_topping(self):
        """Uncheck the topping checkbox."""
        self.uncheck_checkbox(self.TOPPING_CHECKBOX)
    
    def fill_comments(self, comments: str):
        """Fill the comments field."""
        self.fill_input(self.COMMENTS_TEXTAREA, comments)
    
    def submit_form(self):
        """Submit the form."""
        self.click_element(self.SUBMIT_BUTTON)
    
    def fill_form_with_valid_data(self):
        """Fill the form with valid test data."""
        self.fill_customer_name("John Doe")
        self.fill_customer_phone("123-456-7890")
        self.fill_customer_email("john@example.com")
        self.select_pizza_size("large")
        self.check_topping()
        self.fill_comments("Test comment")
    
    def fill_form_with_special_characters(self):
        """Fill the form with special characters."""
        special_text = "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        self.fill_comments(special_text)
    
    def is_customer_name_visible(self) -> bool:
        """Check if customer name field is visible."""
        return self.is_element_visible(self.CUSTOMER_NAME_INPUT)
    
    def is_customer_phone_visible(self) -> bool:
        """Check if customer phone field is visible."""
        return self.is_element_visible(self.CUSTOMER_PHONE_INPUT)
    
    def is_customer_email_visible(self) -> bool:
        """Check if customer email field is visible."""
        return self.is_element_visible(self.CUSTOMER_EMAIL_INPUT)
    
    def is_pizza_size_visible(self) -> bool:
        """Check if pizza size dropdown is visible."""
        return self.is_element_visible(self.PIZZA_SIZE_SELECT)
    
    def is_topping_checkbox_visible(self) -> bool:
        """Check if topping checkbox is visible."""
        return self.is_element_visible(self.TOPPING_CHECKBOX)
    
    def is_comments_visible(self) -> bool:
        """Check if comments textarea is visible."""
        return self.is_element_visible(self.COMMENTS_TEXTAREA)
    
    def is_submit_button_visible(self) -> bool:
        """Check if submit button is visible."""
        return self.is_element_visible(self.SUBMIT_BUTTON)
    
    def get_form_data(self) -> dict:
        """Get the current form data."""
        return {
            'name': self.page.input_value(self.CUSTOMER_NAME_INPUT),
            'phone': self.page.input_value(self.CUSTOMER_PHONE_INPUT),
            'email': self.page.input_value(self.CUSTOMER_EMAIL_INPUT),
            'size': self.page.input_value(self.PIZZA_SIZE_SELECT),
            'topping': self.page.is_checked(self.TOPPING_CHECKBOX),
            'comments': self.page.input_value(self.COMMENTS_TEXTAREA)
        } 