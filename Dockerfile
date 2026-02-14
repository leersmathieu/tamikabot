FROM python:3.12-slim-bookworm

ENV OPENBLAS_NUM_THREADS=1

WORKDIR /opt/app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/app

RUN pip install -r requirements.txt

COPY . /opt/app

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

# CMD ["python", "check_versions.py"]
