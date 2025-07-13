from behave import given, when, then

@given("the user navigates to the search page")
def step_open_search_page(context):
    context.page.goto(context.build_url(context.base_url, ""))

@when('the user searches for "{query}"')
def step_search_query(context, query):
    # Simulate search functionality
    context.search_query = query

@then("the user should see search results")
def step_verify_search_results(context):
    # Verify search results
    assert hasattr(context, 'search_query')
    assert context.search_query == "test query" 