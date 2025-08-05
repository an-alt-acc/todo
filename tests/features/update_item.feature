Feature: Update Item State
  As a user I want to mark items as completed/incomplete so that I can track progress
  
  Scenario: Mark an existing item as complete
    Given the list contains a item with title "Buy Milk" that is incomplete
    When I toggle the item's completion state
    Then the system should confirm the task is marked complete
    And the item's completed status should be true

  Scenario: Mark an existing item as incomplete
    Given the list contains a item with title "Buy Milk" that is complete
    When I toggle the item's completion state
    Then the system should confirm the task is marked incomplete
    And the item's completed status should be false

  Scenario: Attempt to update an item that does not exist
    Given my to-do list is empty
    When I update a non-existent item with ID 123
    Then the system should error saying the item with ID 123 does not exist
