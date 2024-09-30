FROM python:3.9
RUN apt-get update -y
RUN apt-get install -y \
    libpq-dev \
    python3-dev \
    gcc
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir Flask
WORKDIR /app
COPY . .
EXPOSE 5432
ENTRYPOINT ["python", "app.py"]
