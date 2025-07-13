Feature: Contact Form

  Scenario: Submit contact form
    Given the user navigates to the contact page
    When the user fills out the contact form
    Then the user should see a confirmation message 