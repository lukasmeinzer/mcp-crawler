FROM python:3.10-slim


# --- install Node.js and npm ---
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npx

WORKDIR /app

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /app/

# Copy the application into the container.
COPY . /app/

# Install the application dependencies.
WORKDIR /app
RUN uv sync  

# Expose the port the app runs on
EXPOSE 8021

# Run the application.
# CMD ["uv", "run", "streamlit", "run", "app.py", "--port", "8021", "--host", "0.0.0.0"]