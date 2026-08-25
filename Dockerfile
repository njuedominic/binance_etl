FROM python:3.11-slim

#copy uv binary from offcial image
COPY --from=ghcr.io.astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation and set copy mode for Docker mounts
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy project specifications files
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN --mount=type=cache, target=/root/ .cache.uv \
    uv sync --frozen --no-install-project

# Copy the application's source code
COPY . .

# Ensure venv binaries are in PATH
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "main.py"]
CMD ["--symbol", "BTCUSDT"]

