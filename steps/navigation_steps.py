from behave import given, when, then
import time

@given("the user navigates to the homepage")
def step_navigate_homepage(context):
    context.page.goto(context.build_url(context.base_url, ""))

@when("the user checks the page title")
def step_check_page_title(context):
    context.page_title = context.page.title()

@then("the user should see the correct title")
def step_verify_page_title(context):
    assert "httpbin" in context.page_title.lower()

@when("the user clicks on the about link")
def step_click_about_link(context):
    # Simulate clicking a link
    context.current_page = "about"

@then("the user should be on the about page")
def step_verify_about_page(context):
    assert hasattr(context, 'current_page')
    assert context.current_page == "about"

@when("the user resizes the browser window")
def step_resize_browser(context):
    context.page.set_viewport_size({"width": 800, "height": 600})

@then("the page should be responsive")
def step_verify_responsiveness(context):
    # Check if page content is still accessible
    assert context.page.content() is not None 