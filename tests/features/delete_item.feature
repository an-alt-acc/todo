Feature: Delete Item
  As a user I want to delete items so that I can remove tasks I no longer need

  Scenario: Delete an existing item
    Given the list contains items: "Buy Milk"
    When I delete the item "Buy Milk"
    Then the system should confirm the item is deleted
    And the item "Buy Milk" should no longer exist in the list

  Scenario: Attempt to delete an item that does not exist
    Given my to-do list is empty
    When I delete a non-existent item with ID 123
    Then the system should error saying the item with ID 123 does not exist
