# Todo App

## About

The **Todo Application** is a simple task management tool built using **Flask** and **MongoDB**. This app allows users to create, view, update, and delete tasks. Users can log in to their accounts to manage tasks specific to them. The application is designed to be minimalistic, yet functional, for effective task management.

## Features
- **User Authentication**: Secure login and session management.
- **CRUD Operations**: Create, read, update, and delete tasks.
- **MongoDB Integration**: Tasks are stored in a MongoDB database for persistence.
- **Responsive UI**: Clean and simple interface built with HTML, CSS (Bootstrap), and JavaScript.

## Technologies Used
- **Flask** (Python web framework)
- **MongoDB** (NoSQL Database)
- **Bootstrap** (Frontend framework)
- **Python** (Programming language)
- **Jinja2** (Template engine for Python)
- **Flask-WTF** (Form handling and validation)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Todo-App.git

2. **Navigate to the project directory**:
   ```bash
   cd Todo-App

3. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   
4. **Activate the virtual environment**:
   a. On Windows:
   ```bash
   venv\Scripts\activate

   b. **On macOS/Linux**:
   ```bash
   source venv/bin/activate

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

6. **Set up MongoDB**:
   - Create a MongoDB cluster (or use MongoDB Atlas for cloud-hosted MongoDB).
   - Set up the connection string in app.py or your configuration file.

7. **Run the Application**: Run the following command to start the app on port 8000:
   ```bash
   flask run --port=8000
   
8. **Open the app in your browser by going to:**:
   ```bash
   http://127.0.0.1:8000/

## Usage
1. Sign up to create a new user account.
2. Log in to manage your tasks.
3. Add, update, or delete tasks from the main dashboard.
4. Logout to end your session.

## Contributing
1. Fork the repository.
2. Create a new branch (git checkout -b feature-name).
3. Make your changes.
4. Commit your changes (git commit -m 'Added feature').
5. Push to the branch (git push origin feature-name).
6. Open a pull request.
