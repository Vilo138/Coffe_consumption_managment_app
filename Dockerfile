FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install anvil-app-server
RUN pip install -r ./server_code/requirements.txt

EXPOSE 3030

CMD ["anvil-app-server", "--app", "."]
