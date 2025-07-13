Feature: Form Functionality

  @smoke
  Scenario: Fill out contact form
    Given the user navigates to the contact form
    When the user fills out the contact form with valid data
    Then the form should be submitted successfully

  @regression
  Scenario: Validate required fields
    Given the user navigates to the contact form
    When the user tries to submit without filling required fields
    Then the user should see validation errors

  @smoke
  Scenario: Test form with special characters
    Given the user navigates to the contact form
    When the user enters special characters in the form
    Then the form should handle special characters correctly 