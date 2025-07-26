# Use official slim Python image
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir PyMuPDF

CMD ["python", "persona_extractor.py"]
