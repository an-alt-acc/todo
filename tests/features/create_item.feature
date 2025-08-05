Feature: Create Item
  As a user I want to create new items so that I can track my tasks

  Scenario: Create a new item with valid title
    Given my to-do list is empty
    When I add an item with title "Buy Milk"
    Then the system should confirm the item is added
    And the list should contain 1 item with title "Buy Milk"
    And the item is incomplete

  Scenario: Attempt to create an item without a title
    Given my to-do list is empty
    When I add an item with an empty title
    Then the system should error saying the title cannot be empty
    And the item should not be added

