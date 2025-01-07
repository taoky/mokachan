FROM python:3.13-slim

WORKDIR /app
COPY mokachan.py /app/
CMD ["python", "/app/mokachan.py"]
