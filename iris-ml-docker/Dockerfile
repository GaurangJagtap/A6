# Step 1: Use an official lightweight Python image
FROM python:3.11-slim

# Step 2: Set working directory in container
WORKDIR /app

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application code and serialized model
COPY app.py .
COPY model.joblib .

# Step 6: Expose port 5000 for Flask API
EXPOSE 5000

# Step 7: Command to run application on container start
CMD ["python", "app.py"]

