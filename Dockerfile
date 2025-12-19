# Use Python Alpine image for optimized size
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
# Flask and Werkzeug have pre-built wheels, no compilation needed
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    PORT=5000

# Expose the application port
EXPOSE 5000

# Health check using Python
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1

# Run the application
CMD ["python", "app.py"]
