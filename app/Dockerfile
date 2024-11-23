FROM python:3.10-slim

# Set working directory for app
WORKDIR /app
COPY ./app/requirements.txt /app/requirements.txt
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]