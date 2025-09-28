FROM python:3.11-slim
WORKDIR /app
ENV API_PORT=8080
COPY pyproject.toml /app/pyproject.toml
RUN pip install --upgrade pip && pip install -e .
COPY . /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${API_PORT}", "--reload"]
