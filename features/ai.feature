Feature: AI Functionality

  @smoke @ai_healing
  Scenario: Fill out contact form
    Given the user navigates to the contact form
    When the user fills out the contact form with valid data
    Then the form should be submitted successfully