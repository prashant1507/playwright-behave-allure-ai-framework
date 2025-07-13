Feature: Search Functionality

  Scenario: Search for content
    Given the user navigates to the search page
    When the user searches for "test query"
    Then the user should see search results 