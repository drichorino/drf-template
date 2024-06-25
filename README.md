# Django REST APP Template

## Introduction

This template is for a Django REST project that includes basic CRUD user operations, two-factor authentication (2FA), and user logging events.

## Installation

### Prerequisites

- Python 3.12
- Django 5.0.6

### Steps to Deploy on Local Development Environment

1. Clone the repository:
    ```sh
    git clone https://github.com/drichorino/drf-template.git
    cd drf-template
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Rename the `.env.uat.template` file to `.env.uat` and configure it with the appropriate data:
    ```sh
    mv .env.template .env
    ```

    Example contents for `.env.uat` file:
    ```env
    # Environment variables
    SITE_NAME=App Name UAT
    SITE_ABBRV=APP-UAT
    DEBUG=True
    SECRET_KEY=your-uat-secret-key
    DJANGO_ENV=uat

    # Database URL format for MySQL: DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
    DATABASE_URL=mysql://your_db_user:your_db_password@your_db_host:your_db_port/

    # Allowed hosts for production
    ALLOWED_HOSTS=*

    ```

5. Set up the database:
    ```sh
    python manage.py migrate
    ```

6. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Admin interface at `http://127.0.0.1:8000/admin`

## Deployment with Docker

### UAT Deployment

1. Ensure you have Docker and Docker Compose installed on your system.

2. Rename the `.env.uat.template` file to `.env.uat` and configure it with the appropriate data:
    ```sh
    mv .env.uat.template .env.uat
    ```

3. Build and run the Docker container for UAT:
    ```sh
    docker-compose -f docker-compose.uat.yml up -d --build
    ```

4. To stop and remove the UAT containers, networks, and volumes:
    ```sh
    docker-compose -f docker-compose.uat.yml down
    ```

### PROD Deployment

1. Ensure you have Docker and Docker Compose installed on your system.

2. Rename the `.env.prod.template` file to `.env.prod` and configure it with the appropriate data:
    ```sh
    mv .env.prod.template .env.prod
    ```

3. Build and run the Docker container for PROD:
    ```sh
    docker-compose -f docker-compose.prod.yml up -d --build
    ```

4. To stop and remove the PROD containers, networks, and volumes:
    ```sh
    docker-compose -f docker-compose.prod.yml down
    ```