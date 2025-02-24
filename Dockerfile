FROM python:3.11-slim

WORKDIR /app
COPY backend/ /app/

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
