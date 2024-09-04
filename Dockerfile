# Stage 1: Build the FastAPI application
FROM python:3.11-slim AS build

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Stage 2: Final image with the application and PostgreSQL client
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client and any other dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependencies and application code from the build stage
COPY --from=build /app /app

# Expose the port that FastAPI will run on
EXPOSE 8000

# Set the DATABASE_URL environment variable
ENV DATABASE_URL="postgresql+asyncpg://khan:password@db/newtodo"

# Copy the main.py script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make sure the script is executable
RUN chmod +x /app/entrypoint.sh

# Use the Python interpreter to run the main.py script
ENTRYPOINT ["python", "/app/entrypoint.sh"]
