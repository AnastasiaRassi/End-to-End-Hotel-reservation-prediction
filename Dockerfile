FROM python:slim

# Correct ENV syntax
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Correct apt-get clean usage
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Optional: run training pipeline at build time
RUN python pipeline/training_pipeline.py

# Expose port
EXPOSE 5000

# Default command
CMD ["python", "application.py"]
