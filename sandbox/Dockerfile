FROM python:3.11-slim
WORKDIR /app
COPY server.py /app/server.py
RUN pip install --no-cache-dir flask
EXPOSE 3200
CMD ["python", "/app/server.py"]
