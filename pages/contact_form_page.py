from .base_page import BasePage

class ContactFormPage(BasePage):
    URL = "forms/post"
    CUSTOMER_NAME_INPUT = 'input[name="custnames"]' # Correct is 'input[name="custname"]'
    CUSTOMER_PHONE_INPUT = 'input[name="custtels"]' # Correct is 'input[name="custtel"]'
    CUSTOMER_EMAIL_INPUT = 'input[name="custemailx"]' # Correct is 'input[name="custemail"]'
    PIZZA_SIZE_SELECT = 'input[name="size"]'
    TOPPING_CHECKBOX = 'input[name="topping"]'
    DELIVERY_INSTRUCTION_INPUT = 'textarea[name="commentss"]' # Correct is 'textarea[name="comments"]'
    SUBMIT_BUTTON = 'p > button'
    
    def navigate_to_contact_form(self, base_url: str):
        full_url = f"{base_url}/{self.URL}"
        self.navigate_to(full_url)
        self.wait_for_page_load()
    
    def fill_customer_name(self, name: str):
        self.fill_input(self.CUSTOMER_NAME_INPUT, name)
    
    def fill_customer_phone(self, phone: str):
        self.fill_input(self.CUSTOMER_PHONE_INPUT, phone)
    
    def fill_customer_email(self, email: str):
        self.fill_input(self.CUSTOMER_EMAIL_INPUT, email)
    
    def select_pizza_size(self, size: str):
        self.click_element(f"//input[@name='size' and @value='{size}']")
    
    def check_topping(self):
        self.check_checkbox(self.TOPPING_CHECKBOX)
    
    def fill_comments(self, comments: str):
        self.fill_input(self.DELIVERY_INSTRUCTION_INPUT, comments)
    
    def submit_form(self):
        self.click_element(self.SUBMIT_BUTTON)
    
    def fill_form_with_valid_data(self):
        self.fill_customer_name("John Doe")
        self.fill_customer_phone("123-456-7890")
        self.fill_customer_email("john@example.com")
        self.select_pizza_size("large")
        self.check_topping()
        self.fill_comments("Test comment")
    
    def fill_form_with_special_characters(self):
        special_text = "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        self.fill_comments(special_text)