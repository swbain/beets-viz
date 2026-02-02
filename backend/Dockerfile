FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Update the DB path for container
ENV BEETS_DB=/beets/musiclibrary.blb

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
