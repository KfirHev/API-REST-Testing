# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install required packages and Chrome browser
RUN apt-get update && \
    apt-get install -y wget gnupg2 curl && \
    curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable chromium-driver && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of your application code into the container
COPY . .

# Set the display port to avoid crashes in headless mode
ENV DISPLAY=:99

# Set the default command to run tests in Docker
CMD ["pytest", "--run_env=docker", "--maxfail=1", "--disable-warnings", "-v", "--html=Reports/report.html"]
