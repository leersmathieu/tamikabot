FROM python:3.9-slim-buster

WORKDIR /opt/app

COPY requirements.txt /opt/app

RUN pip install -r requirements.txt

COPY . /opt/app

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

# CMD ["python", "check_versions.py"]
