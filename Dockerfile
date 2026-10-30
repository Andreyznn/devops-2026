FROM python:3.14-slim

RUN mkdir /app

WORKDIR /app

#    Host  ->  Contêiner
COPY app.py ./app.py
COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["fastapi", "run"]