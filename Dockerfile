# Use a lightweight Python image based on Alpine Linux
FROM python:3.10-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev postgresql-dev

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . .

# Expose the port your application will run on (default Django port is 8000)
EXPOSE 80

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:80"]
