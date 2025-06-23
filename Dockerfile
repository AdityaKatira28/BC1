# Optimized Dockerfile for Railway deployment with pandas fix
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for potential compilation
# but prioritize using pre-compiled wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel for better package handling
RUN pip install --upgrade pip wheel

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations for wheel usage
# --prefer-binary forces pip to use pre-compiled wheels when available
# --no-cache-dir reduces image size
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

