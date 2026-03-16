FROM python:3.11-slim

WORKDIR /app

# Install CJK fonts for server-side image generation
RUN apt-get update && apt-get install -y --no-install-recommends fonts-wqy-microhei && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir fastapi uvicorn[standard] jinja2 pillow

# Copy application code
COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
