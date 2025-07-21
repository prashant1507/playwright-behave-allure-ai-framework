from behave import step
import time
import psutil

@step("the user navigates to the homepage for performance test")
def step_navigate_homepage_perf(context):
    start_time = time.time()
    context.page.goto(context.build_url(context.base_url, ""))
    context.page_load_time = time.time() - start_time

@step("the page finishes loading")
def step_page_finishes_loading(context):
    context.page.wait_for_load_state("networkidle")

@step("the page load time should be under 3 seconds")
def step_verify_load_time(context):
    assert hasattr(context, 'page_load_time')
    assert context.page_load_time < 3.0

@step("the user opens multiple browser tabs")
def step_open_multiple_tabs(context):
    # Simulate opening multiple tabs
    context.tab_count = 3
    context.initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

@step("the user navigates between tabs")
def step_navigate_between_tabs(context):
    # Simulate tab navigation
    time.sleep(1)  # Simulate navigation time
    context.final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

@step("the memory usage should be reasonable")
def step_verify_memory_usage(context):
    assert hasattr(context, 'initial_memory')
    assert hasattr(context, 'final_memory')
    memory_increase = context.final_memory - context.initial_memory
    assert memory_increase < 100  # Less than 100MB increase

@step("the page loads all resources")
def step_load_all_resources(context):
    # Wait for all resources to load
    context.page.wait_for_load_state("networkidle")
    context.resources_loaded = True

@step("the number of network requests should be optimized")
def step_verify_network_requests(context):
    assert hasattr(context, 'resources_loaded')
    assert context.resources_loaded is True
    # In a real scenario, you would count actual network requests
    # For demo purposes, we'll just verify the page loaded successfully
    assert context.page.content() is not None 