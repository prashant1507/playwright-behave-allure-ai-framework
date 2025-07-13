Feature: Website Navigation

  @smoke
  Scenario: Navigate to homepage
    Given the user navigates to the homepage
    When the user checks the page title
    Then the user should see the correct title

  @regression
  Scenario: Navigate to different pages
    Given the user navigates to the homepage
    When the user clicks on the about link
    Then the user should be on the about page

  @smoke
  Scenario: Check page responsiveness
    Given the user navigates to the homepage
    When the user resizes the browser window
    Then the page should be responsive 