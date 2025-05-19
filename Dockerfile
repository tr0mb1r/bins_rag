# Use Python 3.13 as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pipx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install UV using pipx and ensure it's in PATH
RUN pipx install uv
ENV PATH="/root/.local/bin:${PATH}"

# Verify UV installation
RUN which uv && uv --version

# Copy project files
COPY pyproject.toml .
COPY *.py .
COPY uv.lock .

# Install dependencies directly from pyproject.toml
RUN uv sync

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose the Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.address=0.0.0.0"]