FROM python:3.10-slim

WORKDIR /app


# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app/

# Install the application dependencies.
WORKDIR /app
RUN uv sync  


# Run the application.
CMD ["streamlit", "run", "app.py","--port", "8021", "--host", "0.0.0.0"]