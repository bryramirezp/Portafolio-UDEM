FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install Flask==2.3.3 flask-mysqldb==1.0.1 flask-cors==4.0.0

COPY facturas_service.py .

EXPOSE 5000

CMD ["python", "facturas_service.py"]