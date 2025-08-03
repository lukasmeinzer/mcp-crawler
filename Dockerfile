FROM python:3.10-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv install --no-cache

# Copy the application into the container.
COPY . /app/

# Install the application dependencies.
WORKDIR /app

EXPOSE 8021

CMD ["streamlit", "run", "app.py", "--server.port=8021", "--server.enableCORS=false"]
