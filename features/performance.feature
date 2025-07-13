Feature: Performance Testing

  @performance
  Scenario: Check page load time
    Given the user navigates to the homepage for performance test
    When the page finishes loading
    Then the page load time should be under 3 seconds

  @performance
  Scenario: Test memory usage
    Given the user opens multiple browser tabs
    When the user navigates between tabs
    Then the memory usage should be reasonable

  @performance
  Scenario: Test network requests
    Given the user navigates to the homepage for performance test
    When the page loads all resources
    Then the number of network requests should be optimized 