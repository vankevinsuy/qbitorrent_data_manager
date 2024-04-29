FROM python:3.11.4-alpine3.17

WORKDIR /app

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

CMD [ "python","src/main.py" ]

