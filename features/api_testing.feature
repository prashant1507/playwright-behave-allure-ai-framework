Feature: API Testing

  @api @abc
  Scenario: Test GET request
    Given the user makes a GET request to the API
    When the response is received
    Then the response status should be 200

  @api
  Scenario: Test POST request
    Given the user makes a POST request to the API
    When the response is received
    Then the response status should be 201

  @api
  Scenario: Test API error handling
    Given the user makes an invalid request to the API
    When the response is received
    Then the response status should be 400 