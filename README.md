# To Do List API

Todo List Web Application

## Description

This is a simple RESTful API for a to-do list application. The API is built using FastAPI, SQLAlchemy ORM, PostgreSQL and JWT authentication.

## Features

- Create a new user and user profile
- Login using JWT authentication
- View the list of other user profiles with their tasks
- Create a new task with a title, description, and "is done" flag
- Edit your existing task's details or mark it as completed
- Delete your task from the list
- View a list of all your tasks
- Delete your user, with automatic deletion of user profile and all tasks

## Technologies

- Python
- FastAPI web framework
- SQLAlchemy database toolkit
- PostgreSQL database
- Pytest for testing
- JWT authentication for user authorization

## Installation

1. Clone the repository to your local machine.
2. Create a virtual environment: `virtualenv venv`
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Set up your PostgreSQL database and create the `.env` file with all the necessary configuration variables (check `.env.example`).
5. Run migrations using `.scripts/run_migration.bat`.
6. Start the server using `uvicorn main:app --reload` and navigate to `http://localhost:8000` to use the application.

## API Endpoints

### Authentication
The API requires authentication using JWT tokens. To obtain a token, send a POST request to `/login` with a valid username and password. The API will respond with a token that can be used to authenticate subsequent requests.
Use `/logout` to delete authentication cookies.

### Users
- GET `/users`: Returns a list of all users
- POST `/users`: Creates a new user
- GET `/users/me`: Returns current user's profile
- PATCH `/users/me`: Updates current user's profile
- DELETE `/users/me`: Deletes current user, user's profile, and all user's tasks
- GET `/users/user/{username}`: Returns a specific user by username

### Tasks
- GET `/tasks`: Returns a list of all user's tasks
- POST `/tasks`: Creates a new task
- GET `/tasks/{task_id}`: Returns a specific task by ID
- PATCH `/tasks/{task_id}`: Updates a specific task by ID
- DELETE `/tasks/{task_id}`: Deletes a specific task by ID

### Testing
To run tests for the API, use the command `.scripts/test_myapp.bat`. This will run the automated tests in the `tests/` directory.


## License

This project is licensed under the MIT License - see the `LICENSE` file for details.