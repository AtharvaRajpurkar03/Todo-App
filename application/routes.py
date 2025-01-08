from flask import render_template, request, redirect, flash, url_for
from .forms import TodoForm
from bson import ObjectId
from bson.objectid import ObjectId
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from application import app, db
from application.models import User
from application.extensions import bcrypt
from application.forms import TodoForm
from flask import session




# Show login page as the default route
@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # If already logged in, redirect to dashboard
        return redirect(url_for("view_todos"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check user in database
        user = User.find_by_email(email)

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful!", "success")
            return redirect(url_for("view_todos"))
        else:
            flash("Invalid Email or Password", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user["_id"]), user["email"], user["password"])
    return None

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            flash("Email already exists! Please login.", "danger")
            return redirect(url_for("login"))

        # Create a new user with hashed password
        user_id = User.create_user(email, password)
        flash("Registration Successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")



@app.route("/view_todos", methods=["GET"])
@login_required
def view_todos():
    try:
        # Fetch only tasks belonging to the logged-in user
        todos = db.todos.find({"user_id": current_user.id})  # Filter tasks for the user

        tasks = []
        for todo in todos:
            print(todo)  # Debug log 3 - Print each task matching user ID
            tasks.append({
                "_id": str(todo["_id"]),  # Convert ObjectId to string for HTML usage
                "name": todo["name"],
                "description": todo["description"],
                "completed": todo["completed"],
                "date_created": todo["date_created"].strftime("%Y-%m-%d %H:%M:%S")  # Format date
            })

        # Render the template with filtered tasks
        return render_template("view_todos.html", todos=tasks)

    except Exception as e:
        print("Error occurred:", str(e)) 
        flash("Failed to load tasks!", "danger")
        return redirect(url_for("add_todo"))




@app.route("/add_todo", methods=['GET', 'POST'])
@login_required
def add_todo():
    form = TodoForm()  # Initialize the form

    if form.validate_on_submit():  # Handle POST request
        name = form.name.data
        description = form.description.data
        completed = False

        # Save task to database
        new_task = {
            "user_id": current_user.id,
            "name": name,
            "description": description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }
        db.todos.insert_one(new_task)

        flash("Task added successfully!", "success")
        return redirect(url_for("view_todos"))

    # Handle GET request
    return render_template("add_todo.html", form=form)



@app.route("/update_todo/<id>", methods=["GET", "POST"])
@login_required
def update_todo(id):
    try:
        # Validate ObjectId format
        todo_id = ObjectId(id)  # Convert ID to ObjectId

        # Query for the task belonging to the logged-in user
        todo = db.todos.find_one({
            "_id": todo_id,  # Match task ID
            "user_id": current_user.id  # Match logged-in user ID
        })

        # Handle case where task is not found
        if not todo:
            flash("Todo not found!", "danger")
            return redirect(url_for("view_todos"))

        # Initialize form with existing data
        form = TodoForm(
            name=todo["name"],
            description=todo["description"],
            completed=todo["completed"]
        )

        if form.validate_on_submit():
            # Update the task with new values
            db.todos.update_one(
                {"_id": todo_id},
                {"$set": {
                    "name": form.name.data,
                    "description": form.description.data,
                    "completed": form.completed.data
                }}
            )
            flash("Todo updated successfully!", "success")
            return redirect(url_for("view_todos"))

        return render_template("update_todo.html", form=form, todo=todo)

    except Exception as e:
        flash(f"Error occurred: {str(e)}", "danger")
        return redirect(url_for("view_todos"))


@app.route("/delete_todo/<id>", methods=["POST"])
@login_required
def delete_todo(id):
    try:
        # Validate ObjectId format
        todo_id = ObjectId(id)  # Convert ID to ObjectId

        # Query to ensure the task belongs to the logged-in user
        todo = db.todos.find_one({
            "_id": todo_id,
            "user_id": current_user.id  # Match user ID
        })

        # Handle case where task is not found
        if not todo:
            flash("Todo not found!", "danger")
            return redirect(url_for("view_todos"))

        # Delete the task
        db.todos.delete_one({"_id": todo_id})
        flash("Todo deleted successfully!", "success")
        return redirect(url_for("view_todos"))

    except Exception as e:
        flash(f"Error occurred: {str(e)}", "danger")
        return redirect(url_for("view_todos"))
