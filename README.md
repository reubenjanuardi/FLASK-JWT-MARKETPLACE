# 🛒 FLASK JWT MARKETPLACE API

A secure RESTful marketplace backend built with **Flask**, **JWT authentication**, and **MySQL**.
This API provides authentication, profile management, and CRUD operations for marketplace items.

---

## 📑 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
  - [Authentication](#authentication)
  - [Items](#items)
- [Database Models](#-database-models)
- [Dependencies](#-dependencies)
- [Postman Examples](#-postman-examples)
- [Swagger/OpenAPI Specification](#-swaggeropenapi-specification)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🚀 Introduction

**FLASK-JWT-MARKETPLACE** is a Flask-based API that manages users and marketplace items.
It features secure JWT authentication, token blacklisting, and role-based access for administrative operations.

Use this project as a base for e-commerce, marketplace, or item-management applications.

## ✨ Features

#### Authentication

- User registration and login
- JWT-based authentication with access and refresh tokens
- Token blacklisting for logout
- Automatic token expiration (15 minutes for access tokens, 7 days for refresh tokens)
- Protected routes with JWT verification

#### User Management

- User registration with email and password
- Profile viewing and updating
- Role-based authorization (admin and regular users)
- Secure password hashing

#### Item Management

- CRUD operations for marketplace items
- Public endpoint for viewing items
- Protected endpoints for creating, updating, and deleting items
- Owner/Admin-only access for item modifications

---

## 🗂 Project Structure

```
FLASK-JWT-MARKETPLACE/
├── app.py                # Main Flask application
├── extensions.py         # Extension initialization (DB, JWT, etc.)
├── config/
│   └── database.py       # Database connection setup
├── models/
│   ├── user.py           # User model
│   └── item.py           # Item model
├── migrations/		  # Database table migration
├── routes/
│   ├── auth_routes.py    # Authentication routes
│   └── item_routes.py    # Item CRUD routes
├── requirements.txt      # Dependencies
└── .env                  # Environment variables
```

---

## ⚙️ Installation

1. **Clone repository**

   ```bash
   git clone https://github.com/reubenjanuardi/FLASK-JWT-MARKETPLACE.git
   cd FLASK-JWT-MARKETPLACE
   ```
2. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   Create a `.env` file:

   ```env
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_NAME=marketplace_db
   JWT_SECRET=your_jwt_secret
   ```
5. **Initialize database**

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. **Run the app**

   ```bash
   python app.py
   ```

---

## ⚙️ Configuration

| Variable        | Description           |
| --------------- | --------------------- |
| `DB_USER`     | Database username     |
| `DB_PASSWORD` | Database password     |
| `DB_HOST`     | Database host address |
| `DB_NAME`     | Database name         |
| `JWT_SECRET`  | JWT secret key        |

---

## 🧑‍💻 Usage

Access the API root:

```
GET http://127.0.0.1:5000/
```

Response:

```json
{ "message": "Welcome to JWT Marketplace API" }
```

---

## 🔐 API Endpoints

### **Authentication**

| Method | Endpoint           | Description                  | Auth Required      |
| ------ | ------------------ | ---------------------------- | ------------------ |
| POST   | `/auth/register` | Register new user            | ❌                 |
| POST   | `/auth/login`    | Log in and get tokens        | ❌                 |
| GET    | `/auth/profile`  | Get user profile             | ✅                 |
| PUT    | `/auth/profile`  | Update user profile          | ✅                 |
| POST   | `/auth/logout`   | Logout and blacklist token   | ✅                 |
| POST   | `/auth/refresh`  | Refresh expired access token | ✅ (Refresh Token) |

---

### **Items**

| Method | Endpoint        | Description                    | Auth Required |
| ------ | --------------- | ------------------------------ | ------------- |
| GET    | `/items/`     | Get all items                  | ❌            |
| POST   | `/items/`     | Create new item                | ✅            |
| GET    | `/items/<id>` | Get item by ID                 | ✅            |
| PUT    | `/items/<id>` | Update item (owner/admin only) | ✅            |
| DELETE | `/items/<id>` | Delete item (owner/admin only) | ✅            |

---

## 🧱 Database Models

### **User**

| Field    | Type    | Description                     |
| -------- | ------- | ------------------------------- |
| id       | Integer | Primary key                     |
| name     | String  | User name                       |
| email    | String  | Unique user email               |
| password | String  | Hashed password                 |
| role     | String  | `user` (default) or `admin` |

### **Item**

| Field       | Type    | Description         |
| ----------- | ------- | ------------------- |
| id          | Integer | Primary key         |
| name        | String  | Item name           |
| price       | Float   | Item price          |
| description | Text    | Item description    |
| user_id     | Integer | Foreign key to user |

---

## 📦 Dependencies

```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
Flask-JWT-Extended==4.6.0
Flask-Cors==4.0.0
python-dotenv==1.0.1
PyMySQL==1.1.1
cryptography==43.0.1
Werkzeug==3.0.4
```

---

## 🧪 Postman Examples

### 🔸 Register

**POST** `/auth/register`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "mypassword"
}
```

### 🔸 Login

**POST** `/auth/login`

```json
{
  "email": "john@example.com",
  "password": "mypassword"
}
```

Response:

```json
{
  "message": "Login successful",
  "access_token": "<ACCESS_TOKEN>",
  "refresh_token": "<REFRESH_TOKEN>"
}
```

### 🔸 Create Item

**POST** `/items/`
Headers:

```
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

Body:

```json
{
  "name": "Laptop",
  "price": 1200.00,
  "description": "High-performance laptop"
}
```

### 🔸 Refresh Token

**POST** `/auth/refresh`
Header:

```
Authorization: Bearer <REFRESH_TOKEN>
```

---

## 📘 Swagger/OpenAPI Specification

Example minimal `openapi.yaml`:

```yaml
openapi: 3.0.0
info:
  title: Flask JWT Marketplace API
  version: 1.0.0
  description: A RESTful API for user authentication and marketplace items.
servers:
  - url: http://127.0.0.1:5000
paths:
  /auth/register:
    post:
      summary: Register a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              properties:
                name:
                  type: string
                email:
                  type: string
                password:
                  type: string
      responses:
        '201':
          description: User registered successfully
  /auth/login:
    post:
      summary: User login
      responses:
        '200':
          description: Login successful, returns tokens
  /items/:
    get:
      summary: Retrieve all items
      responses:
        '200':
          description: List of marketplace items
    post:
      summary: Create a new item
      security:
        - bearerAuth: []
      responses:
        '201':
          description: Item created successfully
```

To enable Swagger UI:

```bash
pip install flasgger
```

Then add in `app.py`:

```python
from flasgger import Swagger
swagger = Swagger(app)
```

Open [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---

## 🛠 Troubleshooting

| Issue                         | Possible Cause              | Fix                           |
| ----------------------------- | --------------------------- | ----------------------------- |
| `Invalid token`             | Missing or expired JWT      | Use refresh token or re-login |
| `Unauthorized`              | User not owner or not admin | Check role in DB              |
| `Database connection error` | Wrong `.env` variables    | Verify MySQL credentials      |

---

## 📜 License

This project is licensed under the **MIT License** — you may freely use, modify, and distribute it.
