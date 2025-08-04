from flask import Flask, render_template, request, redirect, url_for
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
# You will likely need a database e.g. DynamoDB so you might either boto3 or pynamodb
# Additional installs here:
import os
import uuid
from dotenv import load_dotenv
#
#

load_dotenv()

app = Flask(__name__)

## Instantiate your database here:
class TaskModel(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = "aws_capstone_project_imx-table"
        region = "ap-southeast-1"

    id = UnicodeAttribute(hash_key=True, null=False, default_for_new=lambda: str(uuid.uuid4()))
    title = UnicodeAttribute(null=False)
    complete = BooleanAttribute(null=False, default_for_new=False)

if not TaskModel.exists():
    print("creating table")
    TaskModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
else:
    print("table is ready")

@app.route("/")
def home():
    # Complete the code below
    # The todo_list variable should be returned by running a scan on your DDB table,
    # which is then converted to a list
    todo_list = list(TaskModel.scan())

    # can leave this line as is to use the template that's provided
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    # Complete code below to create a new item in your todo list
    TaskModel(title=title).save()

    return redirect(url_for("home"))



@app.route("/update/<todo_id>")
def update(todo_id):
    # Complete the code below to update an existing item
    # For this particular app, updating just toggles the completion between True / False
    task = TaskModel.get(todo_id)
    task.complete = not task.complete
    task.save()

    return redirect(url_for("home"))


@app.route("/delete/<todo_id>")
def delete(todo_id):
    # Complete the code below to delete an item from the to-do list
    task = TaskModel.get(todo_id).delete()

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))