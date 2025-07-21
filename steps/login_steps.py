from behave import given, when, then
from playwright.sync_api import expect

@given("the user navigates to the test page")
def step_open_test_page(context):
    test_page = context.page_factory.get_test_page(context)
    test_page.navigate_to_test_page(context.base_url)

@when("the user checks the page content")
def step_check_page_content(context):
    test_page = context.page_factory.get_test_page(context)
    test_page.wait_for_page_load()
    context.page_content = test_page.get_page_content()

@then("the user should see the expected content")
def step_verify_content(context):
    test_page = context.page_factory.get_test_page(context)
    page_content = test_page.get_page_content()
    
    # Use Playwright assertions
    expect(context.page).to_contain_text("httpbin")
    expect(context.page).to_contain_text("get")
    expect(context.page).to_contain_text("post") 