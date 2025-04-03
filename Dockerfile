FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Node.js 20 and npm (required for npx)
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install uvx

# Copy the rest of the application files
COPY . .

# Command to run the application
CMD ["python", "main.py"]