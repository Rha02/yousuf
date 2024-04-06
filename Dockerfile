FROM python:3.11-slim

# Set the working directory
WORKDIR /app

COPY backend/pyproject.toml backend/poetry.lock ./

# Install poetry
RUN pip install poetry

# Copy the rest of the files
COPY backend .

# Install dependencies
RUN cd /app && poetry install

# Run the application
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]