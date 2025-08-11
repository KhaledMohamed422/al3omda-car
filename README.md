# al3omda-car
How to Run This Django Project with PostgreSQL
Prerequisites
Python 3.x installed

PostgreSQL installed and running

pip for Python package management

Virtual environment tool (optional but recommended)

Step 1: Clone the Repository
bash
Copy
Edit
git clone <your-repo-url>
cd <your-repo-folder>
Step 2: Create and Activate a Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Step 3: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Step 4: Setup Environment Variables
Create a .env file in the root of your project with the following content:

env
Copy
Edit
NAME_DB="al3omda_db"
USER_DB="khaled"
PASSWORD_DB="khaled"
HOST_DB="localhost"
PORT_DB="5432"
DEBUG=True
ALLOWED_HOSTS=["*"]
Make sure your Django settings are configured to load these variables from .env. You can use python-dotenv or django-environ for this.

Step 5: Configure Django settings.py
Make sure your settings.py uses these environment variables for the database and other configurations. For example, using os.environ:

python
Copy
Edit
import os
import ast  # To parse string representation of list for ALLOWED_HOSTS

NAME_DB = os.getenv('NAME_DB')
USER_DB = os.getenv('USER_DB')
PASSWORD_DB = os.getenv('PASSWORD_DB')
HOST_DB = os.getenv('HOST_DB')
PORT_DB = os.getenv('PORT_DB')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ast.literal_eval(os.getenv('ALLOWED_HOSTS', '["*"]'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME_DB,
        'USER': USER_DB,
        'PASSWORD': PASSWORD_DB,
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    }
}
Step 6: Setup the PostgreSQL Database
Make sure PostgreSQL is running and you have created the database al3omda_db and the user khaled with the password khaled. You can do this via psql shell:

sql
Copy
Edit
CREATE DATABASE al3omda_db;
CREATE USER khaled WITH PASSWORD 'khaled';
ALTER ROLE khaled SET client_encoding TO 'utf8';
ALTER ROLE khaled SET default_transaction_isolation TO 'read committed';
ALTER ROLE khaled SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE al3omda_db TO khaled;
Step 7: Run Migrations
bash
Copy
Edit
python manage.py migrate
Step 8: Run the Development Server
bash
Copy
Edit
python manage.py runserver
Sample requirements.txt
text
Copy
Edit
Django>=4.0
psycopg2-binary>=2.9
python-dotenv>=0.21.0
