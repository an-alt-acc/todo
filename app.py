from flask import Flask, render_template, request, redirect, url_for
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
# You will likely need a database e.g. DynamoDB so you might either boto3 or pynamodb
# Additional installs here:
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

## Instantiate your database here:
class TaskModel(Model):
    class Meta:
        table_name = os.environ.get("TABLE_NAME", "todo-table")
        region = os.environ.get("REGION", "ap-southeast-1")

    id = UnicodeAttribute(hash_key=True, null=False, default_for_new=lambda: str(uuid.uuid4()))
    title = UnicodeAttribute(null=False)
    complete = BooleanAttribute(null=False, default_for_new=False)
    creation_date = UTCDateTimeAttribute(null=False, default_for_new=lambda: datetime.now())


@app.route("/")
def home():
    # Complete the code below
    # The todo_list variable should be returned by running a scan on your DDB table,
    # which is then converted to a list
    todo_list = list(TaskModel.scan())
    todo_list.sort(key=lambda i: i.creation_date)
    err = request.args.get("err")
    succ = request.args.get("succ")

    # can leave this line as is to use the template that's provided
    return render_template("base.html", todo_list=todo_list, err=err, succ=succ)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    # Complete code below to create a new item in your todo list
    if len(title) == 0:
        return redirect(url_for("home", err="Title cannot be empty"))
    
    TaskModel(title=title).save()

    return redirect(url_for("home", succ="Task added"))



@app.route("/update/<todo_id>")
def update(todo_id):
    # Complete the code below to update an existing item
    # For this particular app, updating just toggles the completion between True / False
    try:
        task = TaskModel.get(todo_id)
    except TaskModel.DoesNotExist:
        return redirect(url_for("home", err=f"Task {todo_id} does not exist"))
    
    task.complete = not task.complete
    task.save()

    return redirect(url_for("home", succ=f"Task marked as {'complete' if task.complete else 'incomplete'}"))


@app.route("/delete/<todo_id>")
def delete(todo_id):
    # Complete the code below to delete an item from the to-do list
    try:
        TaskModel.get(todo_id).delete()
    except TaskModel.DoesNotExist:
        return redirect(url_for("home", err=f"Task {todo_id} does not exist"))

    return redirect(url_for("home", succ=f"Task deleted"))

if __name__ == "__main__":
    if not TaskModel.exists():
        print("creating table")
        TaskModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    else:
        print("table is ready")

    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))