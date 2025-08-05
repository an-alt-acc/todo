import pytest
import uuid

from pytest_bdd import given, parsers
from app import app, TaskModel
from urllib import parse

def get_query_param(url, param):
    return parse.parse_qs(parse.urlparse(url).query)[param][0]

@pytest.fixture
def TestTaskModel():
    TaskModel.Meta.table_name = f"test_table_{uuid.uuid4()}"

    if not TaskModel.exists():
        TaskModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    yield TaskModel

    if TaskModel.exists():
        TaskModel.delete_table()


@pytest.fixture(scope="session")
def client():
    app.config.update({"TESTING": True})
    return app.test_client()


@given("my to-do list is empty")
def _(TestTaskModel: type[TaskModel]):
    assert len(list(TestTaskModel.scan())) == 0

@given(parsers.parse('the list contains items: {titles}'), target_fixture="pre_added_items")
def _(TestTaskModel: type[TaskModel], titles):
    titles = [t.strip('"') for t in titles.split(", ")]
    items = []
    for title in titles:
        item = TestTaskModel(title=title)
        item.save()
        items.append(item)
    assert len(list(TestTaskModel.scan())) == len(titles)
    return items