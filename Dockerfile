FROM python:3.12.0-slim-bullseye

WORKDIR /python-docker

RUN pip3 install python-dotenv

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./flaskr .

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]