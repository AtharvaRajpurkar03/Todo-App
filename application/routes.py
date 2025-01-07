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
@login_required  # Requires login
def view_todos():
    todos = db.todos.find({"user_id": current_user.id})  # Show only user-specific tasks
    return render_template("view_todos.html", todos=todos)


@app.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    # Get form data
    name = request.form.get("name")
    description = request.form.get("description")
    completed = False  # Default value for completion status

    # Link task associated with the logged-in user
    new_task = {
        "user_id": current_user.id,  # Store user ID for task ownership
        "name": name,
        "description": description,
        "completed": completed,
        "date_created": datetime.utcnow()
    }
    db.todos.insert_one(new_task)  # Save to database

    flash("Task added successfully!", "success")
    return redirect(url_for("view_todos"))

@app.route("/update_todo/<id>", methods=["GET", "POST"])
@login_required
def update_todo(id):
    # Find the todo by ID and user
    todo = db.todos.find_one({"_id": ObjectId(id), "user_id": current_user.id})

    if not todo:
        flash("Todo not found!", "danger")
        return redirect(url_for("view_todos"))

    # Initialize form with existing values
    form = TodoForm(
        name=todo["name"],
        description=todo["description"],
        completed=todo["completed"]
    )

    if request.method == "POST" and form.validate_on_submit():
        # Explicitly check for the value of completed
        completed_status = form.completed.data  # Fetch true or false directly

        # Update the task in MongoDB
        db.todos.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": form.name.data,
                "description": form.description.data,
                "completed": completed_status  # Explicitly update status
            }}
        )

        flash("Todo updated successfully!", "success")
        return redirect(url_for("view_todos"))

    # Render update form with pre-filled values
    return render_template("update_todo.html", form=form, todo=todo)



@app.route("/delete_todo/<id>", methods=["POST"])  # Accept POST instead of DELETE
@login_required
def delete_todo(id):
    # Find the todo by ID and user
    todo = db.todos.find_one({"_id": ObjectId(id), "user_id": current_user.id})

    if not todo:
        flash("Todo not found!", "danger")
        return redirect(url_for("view_todos"))

    # Delete the todo
    db.todos.delete_one({"_id": ObjectId(id)})
    flash("Todo deleted successfully!", "success")

    # Redirect back to view todos
    return redirect(url_for("view_todos"))

