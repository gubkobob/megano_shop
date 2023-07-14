FROM python:3.10

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app/

CMD ["python", "manage.py", "runserver", "127.0.0.0:8000"]