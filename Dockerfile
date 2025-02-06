FROM python:3.14.0a4-alpine3.21
WORKDIR /app

RUN apt update && apt upgrade -y && apt autoremove -y
RUN apt update && apt install curl -y && rm -rf /var/lib/apt/lists/* && apt clean

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN python -m venv venv
ENV PYTHONPATH="$PYTHONPATH:/app/venv/lib/python3.14/site-packages"
RUN /app/venv/bin/pip install -r ./requirements.txt

CMD ["/app/venv/bin/python", "src/main.py"]