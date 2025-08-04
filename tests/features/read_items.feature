Feature: Read Items
  As a user I want to view my items so that I can review my tasks

  Scenario: View all items in the list
    Given the list contains items: "Buy Milk", "Call Mom"
    When I load the page
    Then I should see 2 items in the list
    And the item in position 1 has title "Buy Milk"
    And the item in position 2 has title "Call Mom"

