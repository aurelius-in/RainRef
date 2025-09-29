FROM python:3.11-slim
WORKDIR /app
ENV API_PORT=8080
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
# Run migrations on container start, then start API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
