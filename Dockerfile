FROM python:3.12-slim-bookworm

ENV OPENBLAS_NUM_THREADS=1

WORKDIR /opt/app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg curl ca-certificates gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install -y nodejs && \
    apt-get remove -y curl gnupg && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/app

RUN pip install -r requirements.txt && \
    pip install -U bgutil-ytdlp-pot-provider && \
    touch /usr/local/lib/python3.12/site-packages/yt_dlp_plugins/__init__.py && \
    touch /usr/local/lib/python3.12/site-packages/yt_dlp_plugins/extractor/__init__.py

COPY . /opt/app

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

# CMD ["python", "check_versions.py"]
