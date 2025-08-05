from flask.testing import FlaskClient
from pytest_bdd import scenarios, given, when, then, parsers
from app import TaskModel
from werkzeug.test import TestResponse

from tests.steps.conftest import get_query_param

scenarios("../features/create_item.feature")


@when(parsers.parse('I add an item with title "{title}"'), target_fixture="add_response")
def _(client: FlaskClient, title):
    response = client.post("/add", data={"title": title})
    assert response.status_code == 302
    return response


@then(parsers.parse('the system should confirm the item is added'))
def _(add_response: TestResponse):
    assert get_query_param(add_response.location, "succ") == "Task added"


@then(parsers.parse('the list should contain 1 item with title "{title}"'), target_fixture="added_item")
def _(TestTaskModel: type[TaskModel], title):
    items = list(TestTaskModel.scan())
    assert len(items) == 1
    assert items[0].title == title
    return items[0]

@then(parsers.parse('the item is incomplete'))
def _(added_item: TaskModel):
    assert not added_item.complete

@when(parsers.parse('I add an item with an empty title'), target_fixture="bad_add_response")
def _(client: FlaskClient):
    response = client.post("/add", data={"title": ""})
    return response

@then(parsers.parse('the system should error saying the title cannot be empty'))
def _(bad_add_response: TestResponse):
    assert get_query_param(bad_add_response.location, "err") == "Title cannot be empty"

@then(parsers.parse('the item should not be added'))
def _(TestTaskModel: type[TaskModel]):
    assert len(list(TestTaskModel.scan())) == 0
