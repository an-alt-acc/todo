from flask.testing import FlaskClient
from pytest_bdd import scenarios, given, when, then, parsers
from app import TaskModel
from werkzeug.test import TestResponse

from tests.steps.conftest import get_query_param

scenarios("../features/delete_item.feature")


@when(parsers.parse('I delete the item "{title}"'), target_fixture="delete_response")
def _(TestTaskModel: type[TaskModel], client: FlaskClient, title):
    item_id = next(i.id for i in TestTaskModel.scan() if i.title == title)
    response = client.get(f"/delete/{item_id}")
    assert response.status_code == 302
    return response


@when(parsers.parse('I delete a non-existent item with ID {id_}'), target_fixture="delete_response2")
def _(client: FlaskClient, id_):
    response = client.get(f"/delete/{id_}")
    assert response.status_code == 302
    return response


@then(parsers.parse('the system should confirm the item is deleted'))
def _(delete_response: TestResponse):
    assert get_query_param(delete_response.location, "succ") == "Task deleted"


@then(parsers.parse('the item "{title}" should no longer exist in the list'))
def _(TestTaskModel: type[TaskModel], title):
    assert all(i.title != title for i in TestTaskModel.scan())


@then(parsers.parse('the system should error saying the item with ID {id_} does not exist'))
def _(delete_response2: TestResponse, id_):
    assert get_query_param(delete_response2.location, "err") == f"Task {id_} does not exist"





