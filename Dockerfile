# Use a lightweight Python image
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set working dir
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies using uv
RUN uv sync --no-dev --frozen --system

# Expose FastAPI port
EXPOSE 8000

# Start the app
CMD ["uv", "run", "uvicorn", "fjorden.main:app", "--host", "0.0.0.0", "--port", "8000"]
