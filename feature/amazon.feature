Feature: Add product and validate
  As a tester, i am going to validate the amount for toys

  Scenario: Add Toys into cart and validate
    Given I will launch a Browser in chrome
    When I will search toys
    Then I will Select any 2 products and add to cart and validate the price
