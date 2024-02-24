FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install  -r requirements.txt

COPY . .

WORKDIR /usr/src/app/note_it

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]