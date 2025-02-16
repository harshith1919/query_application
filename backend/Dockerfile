# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

COPY requirements.txt /app/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose the application port
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
