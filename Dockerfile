# Phygital Engram, server version. Works on amd64 and arm64.
# Build context: the whole repository (see .dockerignore). The search program (engram.py, engram_lib/, config.json)
# must be in it.
FROM python:3.14-slim-trixie

WORKDIR /app

# dependencies first, so code changes rebuild fast
COPY requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements-server.txt

COPY . /app

RUN chmod +x /app/docker-entrypoint.sh \
 && useradd --system --uid 10001 --home-dir /data app \
 && mkdir -p /data /notes && chown 10001:10001 /data

# Your notes are mounted read-only at /notes. Everything that must survive a restart lives in /data.
ENV HOST=0.0.0.0 \
    PORT=8765 \
    ENGRAM_VAULT=/notes \
    ENGRAM_DATA=/data \
    PHYGITAL_ENGRAM_TRUST_PROXY=1
VOLUME ["/data"]
EXPOSE 8765

HEALTHCHECK --interval=60s --timeout=5s CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\", \"8765\")}/health')"

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "/app/mcp/serve.py"]
