FROM python:3

WORKDIR /usr/src/app

EXPOSE 5000

COPY requirements.txt ./
RUN apt-get update -y && \
    apt-get upgrade -y --no-install-recommends && \
    pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* 

COPY . .

CMD [ "python", "./app.py" ]
