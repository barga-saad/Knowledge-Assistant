FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and CA certificates
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

# Copy application
COPY . .

# Create documents directory
RUN mkdir -p documents

# Run migrations and start app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
