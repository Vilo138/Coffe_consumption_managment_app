FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install --upgrade pip
RUN pip install anvil-app-server
RUN pip install -r requirements.txt

CMD ["anvil-app-server", "--app", "."]
