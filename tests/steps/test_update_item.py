from flask.testing import FlaskClient
from pytest_bdd import scenarios, given, when, then, parsers
from app import TaskModel
from werkzeug.test import TestResponse
from bs4 import BeautifulSoup, ResultSet, Tag

from tests.steps.conftest import get_query_param

scenarios("../features/update_item.feature")

@given(parsers.parse('the list contains a item with title "{title}" that is {state}'), target_fixture="task_id")
def _(TestTaskModel: type[TaskModel], title, state):
    if state == "complete":
        complete = True
    elif state == "incomplete":
        complete = False
    else:
        raise ValueError(f"invalid state `{state}`")
    task = TestTaskModel(title=title, complete=complete)
    task.save()
    assert len(list(TestTaskModel.scan())) == 1
    return task.id


@when("I toggle the item's completion state", target_fixture="update_response")
def _(client: FlaskClient, task_id):
    response = client.get(f"/update/{task_id}")
    assert response.status_code == 302
    return response


@then(parsers.parse("the system should confirm the task is marked {state}"))
def _(update_response: TestResponse, state):
    assert get_query_param(update_response.location, "succ") == f"Task marked as {state}"

@then(parsers.parse("the item's completed status should be {status_str}"))
def _(TestTaskModel: type[TaskModel], task_id, status_str):
    if status_str == "true":
        status = True
    elif status_str == "false":
        status = False
    else:
        raise ValueError(f"Invalid status {status}")
    
    assert TestTaskModel.get(task_id).complete == status


@when(parsers.parse('I update a non-existent item with ID {id_}'), target_fixture="update_response2")
def _(client: FlaskClient, id_):
    response = client.get(f"/update/{id_}")
    assert response.status_code == 302
    return response


@then(parsers.parse('the system should error saying the item with ID {id_} does not exist'))
def _(update_response2: TestResponse, id_):
    assert get_query_param(update_response2.location, "err") == f"Task {id_} does not exist"

