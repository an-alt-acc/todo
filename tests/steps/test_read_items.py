from flask.testing import FlaskClient
from pytest_bdd import scenarios, given, when, then, parsers
from app import TaskModel
from werkzeug.test import TestResponse
from bs4 import BeautifulSoup, ResultSet, Tag

scenarios("../features/read_items.feature")




@when("I load the page", target_fixture="page_response")
def _(client):
    response = client.get("/")
    assert response.status_code == 200
    return response


@then(parsers.parse("I should see {count:d} items in the list"), target_fixture="html_items")
def _(page_response: TestResponse, count):
    html = BeautifulSoup(page_response.data, features="html.parser")
    items = html.select(".ui.segment > .ui.big.header")
    assert len(items) == count
    return items

@then(parsers.parse('the item in position {pos:d} has title "{title}"'))
def _(html_items: ResultSet[Tag], pos, title):
    assert html_items[pos-1].string == title
