FROM python:3

ADD ./Breakout/ /

RUN pip install pygame

CMD [ "python", "./main.py" ]
