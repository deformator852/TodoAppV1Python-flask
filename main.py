import re
import sqlite3
from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = "324asdf1322pasdkjj1`23nj"


def connect_db():
    db = sqlite3.connect("todo.db")
    return db.cursor()


def data_validation(data):
    todo_title = data.form["todo_title"]
    todo_due_date = data.form["todo_due_date"]
    validation = []

    if len(todo_title) >= 3:
        validation.append(True)
    else:
        flash("Length title too litle")
        validation.append(False)

    if todo_title.isalpha():
        validation.append(True)
    else:
        flash("Some symbol in title not alphabetic")
        validation.append(False)

    if re.search(r"\d\d.\d\d.\d\d\d\d$", todo_due_date):
        validation.append(True)
    else:
        flash("Something wrong in due date")
        validation.append(False)

    return all(validation)


@app.route("/")
def index():
    db = connect_db()
    try:
        todo_list = db.execute("SELECT id,title,due_date,status FROM todo ORDER BY status, due_date DESC, title")
    except:
        db.close()
    return render_template("index.html", todo_list=todo_list)


@app.route("/done_todo/<int:todo_id>")
def done_todo(todo_id):
    db = connect_db()
    db.execute(f"UPDATE todo SET status = 'done' WHERE id={todo_id}")
    db.connection.commit()
    db.close()
    return redirect("/")


@app.route("/delete_todo/<int:todo_id>")
def delete_todo(todo_id):
    db = connect_db()
    db.execute(f"DELETE from todo WHERE id = {todo_id}")
    db.connection.commit()
    db.close()
    return redirect("/")


@app.route("/create_todo", methods=["POST", "GET"])
def create_todo():
    if request.method == "POST":
        database = connect_db()
        todo_title = request.form["todo_title"]
        todo_due_date = request.form["todo_due_date"]
        if data_validation(request):
            query = f"""
            INSERT INTO todo (title, due_date, status) VALUES (?,?,?);
            """
            database.execute(query, (todo_title, todo_due_date, "do"))
            database.connection.commit()
            database.close()
            print("data add successfully")
    return redirect(url_for("index"))


@app.route("/<filter>")
def filter_index(filter):
    db = connect_db()
    if filter == "do":
        try:
            todo_list = db.execute(
                "SELECT id,title,due_date,status FROM todo WHERE status = 'do' ORDER BY status, due_date DESC, title")
            return render_template("index.html", todo_list=todo_list, filter="do")
        except:
            db.close()
    elif filter == "done":
        try:
            todo_list = db.execute(
                "SELECT id,title,due_date,status FROM todo WHERE status = 'done' ORDER BY status, due_date DESC, title")
        except:
            db.close()
        return render_template("index.html", todo_list=todo_list)


if __name__ == "__main__":
    app.run(debug=True)
