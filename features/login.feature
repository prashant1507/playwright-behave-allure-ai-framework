Feature: Website Navigation

  @abc
  Scenario: Navigate to a test website
    Given the user navigates to the test page
    When the user checks the page content
    Then the user should see the expected content 