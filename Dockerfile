FROM python:3.10-slim

WORKDIR /app

# -------------------------------
# Install system dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    gnupg \
    ca-certificates \
    curl \
    build-essential \
    wget

# -------------------------------
# Install Node.js and npm (LTS)
# -------------------------------
RUN wget -qO- https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Confirm versions (for debugging)
RUN node -v && npm -v && npx --version

# -------------------------------
# Install uv
# -------------------------------
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# -------------------------------
# Copy project files
# -------------------------------
COPY pyproject.toml uv.lock /app/
RUN uv sync

COPY . /app/

# -------------------------------
# Expose port 
# -------------------------------
EXPOSE 8021
