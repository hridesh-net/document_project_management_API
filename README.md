# Document & Project Management API

A RESTful API built with FastAPI that supports user authentication via JWT, role-based access control (RBAC), and CRUD operations on projects and documents. The API leverages SQLModel with PostgreSQL for data storage and Alembic(Optional) for database migrations.


## Features
- User Authentication:
Secure user registration and login using JWT tokens.

- Role-Based Access Control (RBAC):
Granular permissions with roles and permissions (admin and user).

- Admin: Full create, read, update, and delete permissions.

- User: Read-only access.

- CRUD Operations:
Manage projects and documents through dedicated endpoints.

- Database Migrations:
Alembic integration to handle schema changes safely.

- Interactive Documentation:
Automatically generated API docs using Swagger UI.

## Technology Stack
- Python 3.12
- FastAPI
- SQLModel (with PostgreSQL)
- Alembic
- Uvicorn
- PostgreSQL

## Getting Started

### Prerequisites
- Python 3.12
- PostgreSQL

### Installation
1. Clone the Repository:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. Create a Virtual Environment & Activate It:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Environment Variables:
Create a .env file in the project root and add:

```.env
DATABASE_URL=postgresql://username:password@localhost/yourdbname
JWT_SECRET=your_jwt_secret
```


### Database Setup & Migrations
1. Initialize the Database:
Ensure your PostgreSQL server is running and the specified database exists.
2. Run Migrations: Migration will run automatically but if not you can use optional Alembic migration

```bash
alembic upgrade head
```

3. Seed Roles and Permissions (Optional):
Run the seeding script to populate initial roles and permissions:

```bash
python seed.py
```

## Running the Server

1. Start the FastAPI server with:

```bash
uvicorn app.main:app --reload
```

2. Access the interactive API documentation at http://127.0.0.1:8000/docs.

⸻

## API Endpoints

1. Authentication
    - POST /register: Register a new user.
    - POST /login: Log in to receive a JWT token.

2. Projects
	- GET /projects: Retrieve all projects.
	- POST /projects: Create a new project (requires “create” permission).
	- PUT /projects/{project_id}: Update an existing project (requires “update” permission).
	- DELETE /projects/{project_id}: Delete a project (requires “delete” permission).

3. Documents
	- GET /documents: Retrieve all documents.
	- POST /documents: Create a new document (requires “create” permission).
	- PUT /documents/{document_id}: Update a document (requires “update” permission).
	- DELETE /documents/{document_id}: Delete a document (requires “delete” permission).


## Testing

- Run your tests using pytest:

```bash
pytest
```

- You can also import the provided Postman collection (see postman_collection.json) to manually test the endpoints.


## Demo

![Demo Video](static/demo.gif)
