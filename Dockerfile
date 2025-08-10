# Use the official Python image (works for both AMD64 and ARM64)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Expose port for FastAPI
EXPOSE 8000



# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


