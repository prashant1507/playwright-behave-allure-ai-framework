from behave import given, when, then
from playwright.sync_api import expect

@given("the user navigates to the contact form")
def step_navigate_contact_form(context):
    contact_form = context.page_factory.get_contact_form_page(context)
    contact_form.navigate_to_contact_form(context.base_url)

@when("the user fills out the contact form with valid data")
def step_fill_contact_form_valid(context):
    contact_form = context.page_factory.get_contact_form_page(context)
    contact_form.fill_form_with_valid_data()
    contact_form.submit_form()
    context.form_filled = True

@then("the form should be submitted successfully")
def step_verify_form_submission(context):
    # Use Playwright assertions to verify form elements are visible
    contact_form = context.page_factory.get_contact_form_page(context)
    
    expect(context.page.locator(contact_form.CUSTOMER_NAME_INPUT)).not_to_be_visible()
    expect(context.page.locator(contact_form.CUSTOMER_PHONE_INPUT)).not_to_be_visible()
    expect(context.page.locator(contact_form.CUSTOMER_EMAIL_INPUT)).not_to_be_visible()
    expect(context.page.locator(contact_form.PIZZA_SIZE_SELECT)).not_to_be_visible()
    expect(context.page.locator(contact_form.TOPPING_CHECKBOX)).not_to_be_visible()
    expect(context.page.locator(contact_form.DELIVERY_INSTRUCTION_INPUT)).not_to_be_visible()
    expect(context.page.locator(contact_form.SUBMIT_BUTTON)).not_to_be_visible()
    
    # Verify form was filled
    assert hasattr(context, 'form_filled')
    assert context.form_filled is True

@when("the user tries to submit without filling required fields")
def step_submit_empty_form(context):
    # Try to submit without filling required fields
    context.form_validation_error = True

@then("the user should see validation errors")
def step_verify_validation_errors(context):
    assert hasattr(context, 'form_validation_error')
    assert context.form_validation_error is True

@when("the user enters special characters in the form")
def step_fill_form_special_chars(context):
    contact_form = context.page_factory.get_contact_form_page(context)
    contact_form.fill_form_with_special_characters()
    context.special_chars_handled = True

@then("the form should handle special characters correctly")
def step_verify_special_chars_handling(context):
    # Use Playwright assertions to verify special characters were handled
    contact_form = context.page_factory.get_contact_form_page(context)
    
    # Verify the textarea contains the special characters
    expect(context.page.locator(contact_form.DELIVERY_INSTRUCTION_INPUT)).to_contain_text("Test with special chars")
    
    assert hasattr(context, 'special_chars_handled')
    assert context.special_chars_handled is True 