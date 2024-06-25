FROM python:3.12.4-alpine3.20

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    linux-headers \
    pkgconf

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Set the working directory to the Django project root (where manage.py is located)
WORKDIR /app/def_template

# Expose the port the app runs on
EXPOSE 8000

# # Run the application using Waitress
# CMD ["waitress-serve", "--port=8000", "core.wsgi:application"]
