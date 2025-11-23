# Base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and using stdout buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system libs required for:
# - mysqlclient
# - Pillow (JPEG, zlib)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-mysql-client \
    default-libmysqlclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && apt-get clean

# Copy requirement file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . /app/

# Collect static files (WhiteNoise will serve them)
RUN python manage.py collectstatic --noinput

# Expose Django/Gunicorn port
EXPOSE 8000

# Run the app using Gunicorn
CMD ["gunicorn", "portfolioproject.wsgi:application", "--bind", "0.0.0.0:8000"]
