# Blogging Platform API

![Blogging Platform API](https://assets.roadmap.sh/guest/todo-list-api-bsrdd.png)

This project provides a RESTful API interface that allows users to perform CRUD operations on their to-do items. It also implements JWT for user authentication and handles error management. The project uses [FastAPI](https://fastapi.tiangolo.com/) and [MySQL](https://www.mysql.com/), and utilizes an ORM to interact with the database.

NOTE: This project does not implement a frontend client. The backend web service sends/recieves posts in JSON form. 

## Goals
The goals of this project are to:
- Demonstrate RESTful APIs and their best practices and conventions
- Demonstrate CRUD operations using an Object Relational Model (ORM)
- Implement JSON Web Token (JWT) for user authentication and authorization
- Handle common errors and provide meaningful error responses for better user experience

## Features
The RESTful API allows users to perform the following operations:
- Register a new user
- Log in a user
- Create a new to-do item
- Retrieve a single to-do item
- Retrieve all to-do items
- Update an existing to-do item
- Delete an existing to-do item

## Usage
### Locally (Use [Pip or Poetry](#Install) Install Dependencies)
```
git clone https://github.com/ericcarry88828/Todo-List-API.git
cd Todo-List-API/backend
alembic upgrade head
uvicorn main:app
```
### Docker
```
git clone https://github.com/ericcarry88828/Todo-List-API.git
cd Todo-List-API
docker compose up
```

## Install
### Pip
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
### Poetry
```
poetry install
.\.venv\Scripts\activate
```


## Environment Variables
- `backend/prod.env` for MySQL and the backend in the production environment
    - `MYSQL_ROOT_PASSWORD`
    - `MYSQL_HOST`
    - `MYSQL_USER`
    - `MYSQL_PASSWORD`
    - `MYSQL_DATABASE`
    - `MYSQL_PORT`
    - `MYSQL_DRIVER`
- `backend/dev.env` for MySQL and the backend in the development environment
    - `MYSQL_HOST`
    - `MYSQL_USER`
    - `MYSQL_PASSWORD`
    - `MYSQL_DATABASE`
    - `MYSQL_PORT`
    - `MYSQL_DRIVER`

## Examples

### User Registration
Register a new user using the following request:

```json
POST /register
{
  "name": "John Doe",
  "email": "john@doe.com",
  "password": "password"
}
```

This will validate the given details, make sure the email is unique and store the user details in the database. Make sure to hash the password before storing it in the database.

```json
{
    "message": "Registration successful"
}
```

### User Login
Authenticate the user using the following request:

```json
POST /login
{
  "email": "john@doe.com",
  "password": "password"
}
```
This will validate the given email and password, and respond with a token if the authentication is successful.

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
}
```

### Create a To-Do Item
Create a new to-do item using the following request:

```josn
POST /todos
{
  "title": "Buy groceries",
  "description": "Buy milk, eggs, and bread"
}
```
User must send the token received from the login endpoint in the header to authenticate the request. You can use the Authorization header with the token as the value. In case the token is missing or invalid, respond with an error and status code 401.

```josn
{
  "message": "Unauthorized"
}
```

Upon successful creation of the to-do item, respond with the details of the created item.

```josn
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Buy milk, eggs, and bread"
}
```

### Update a To-Do Item
Update an existing to-do item using the following request:

```json
PUT /todos/1
{
  "title": "Buy groceries",
  "description": "Buy milk, eggs, bread, and cheese"
}
```

Just like the create todo endpoint, user must send the token received. Also make sure to validate the user has the permission to update the to-do item i.e. the user is the creator of todo item that they are updating. Respond with an error and status code 403 if the user is not authorized to update the item.

```json
{
  "message": "Forbidden"
}
```

Upon successful update of the to-do item, respond with the updated details of the item.

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Buy milk, eggs, bread, and cheese"
}
```

### Delete a To-Do Item
Delete an existing to-do item using the following request:
```
DELETE /todos/1
```
User must be authenticated and authorized to delete the to-do item. Upon successful deletion, respond with the status code 204.

### Get To-Do Items
Get the list of to-do items using the following request:

```
GET /todos?page=1&limit=10
```
User must be authenticated to access the tasks and the response should be paginated. Respond with the list of to-do items along with the pagination details.

```json
{
  "data": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Buy milk, eggs, bread"
    },
    {
      "id": 2,
      "title": "Pay bills",
      "description": "Pay electricity and water bills"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 2
}
```

This project idea was provided by [Roadmap](https://roadmap.sh/projects/todo-list-api).
