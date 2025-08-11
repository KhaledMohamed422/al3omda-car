# How to Run This Django Project with PostgreSQL

## Prerequisites

- Python 3.x installed
- PostgreSQL installed and running
- `pip` for Python package management
- Virtual environment tool (optional but recommended)

---

## Step 1: Clone the Repository


```
git clone <your-repo-url>
cd <your-repo-folder>
```

---

## Step 2: Create and Activate a Virtual Environment (Optional but Recommended)

```
python3 -m venv venv
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```
---

## Step 3: Install Dependencies

`pip install -r requirements.txt`

---

## Step 4: Setup Environment Variables

Create a `.env` file in the root of your project with the following content:

```
NAME_DB="al3omda_db"
USER_DB="khaled"
PASSWORD_DB="khaled"
HOST_DB="localhost"
PORT_DB="5432"
DEBUG=True
ALLOWED_HOSTS=["*"]
```


Make sure your Django settings are configured to load these variables from `.env`. You can use `python-dotenv` or `django-environ` for this.

---

## Step 5: Setup the PostgreSQL Database


Make sure PostgreSQL is running and you have created the database `al3omda_db` and the user `khaled` with the password `khaled`. You can do this via psql shell:

```SQL
CREATE DATABASE al3omda_db;
CREATE USER khaled WITH PASSWORD 'khaled';
ALTER ROLE khaled SET client_encoding TO 'utf8';
ALTER ROLE khaled SET default_transaction_isolation TO 'read committed';
ALTER ROLE khaled SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE al3omda_db TO khaled;
```

---

## Step 7: Run Migrations and Migrate

```python
python3 manage.py makemigrations
python3 manage.py migrate
```

---
## Step 7: Run the Development Server

`python manage.py runserver`

