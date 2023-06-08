FROM python:3.9-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code

# This is for development 
ENTRYPOINT ["flask", "--app", "app" ,"run", "--debug", "-p", "8081", "--host", "0.0.0.0"]

# this is for production 
# ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8081", "app:app"]
 
