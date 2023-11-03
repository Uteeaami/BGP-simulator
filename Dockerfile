
FROM python:3.8

ENV DOCKER_ENV=true

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y uml-utilities net-tools iproute2

COPY . .

CMD ["python", "main.py"]
