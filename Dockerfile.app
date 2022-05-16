FROM python:3.8-buster

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app ./app
COPY ./db ./db
COPY ./static ./static
COPY ./main_app.py ./main_app.py

CMD [ "python3", "main_app.py" ]