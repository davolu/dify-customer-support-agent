FROM python:3.13-slim
WORKDIR /app
COPY server.py ./
COPY orders ./orders
EXPOSE 8000
CMD ["python", "server.py"]
