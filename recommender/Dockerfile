FROM python:3.10-slim

# Set working directory for recommender
WORKDIR /recommender
COPY ./recommender/requirements.txt /recommender/requirements.txt
COPY ./recommender /recommender

# Install dependencies
RUN pip install -r /recommender/requirements.txt

# Set up the app to run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8081"]