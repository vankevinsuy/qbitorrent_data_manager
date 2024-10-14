FROM python:3.12.7-slim-bullseye
WORKDIR /app

RUN apt update && apt upgrade -y && apt autoremove -y
RUN apt update && apt install curl -y && rm -rf /var/lib/apt/lists/* && apt clean

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
CMD ["python", "src/main.py"]

