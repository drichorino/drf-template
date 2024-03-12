
# DRF Template

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python (3.8, 3.9, or 3.10)
- pip (Python package manager)
- Virtual environment (optional but recommended)

### Setting Up the Project

1. **Clone the Repository**

   Start by cloning the project repository to your local machine.

git clone https://github.com/drichorino/hris-be
cd hris-be


2. **Create and Activate a Virtual Environment** (Optional but recommended)

- On Windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```

- On macOS and Linux:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install Requirements**

Install all project dependencies by running:

pip install -r requirements.txt


### Configuring the Database

This project uses SQLite by default, so no additional configuration is needed for a quick start. However, if you're using a different database (e.g., PostgreSQL, MySQL), make sure to configure your database settings in `your_project_name/settings.py` accordingly.

### Applying Migrations

Django uses migrations to propagate changes you make to your models (adding a field, deleting a model, etc.) into your database schema. To apply migrations, run:

python manage.py migrate


This command looks at the `INSTALLED_APPS` setting and creates any necessary database tables according to the database settings in your `settings.py` file and the database migrations shipped with the app.

### Running the Development Server

To start the Django development server, run:

python manage.py runserver