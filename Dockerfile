FROM python:3.9-slim-buster

WORKDIR /opt/app

COPY . /opt/app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]