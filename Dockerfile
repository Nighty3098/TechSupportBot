FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/resources

ENV PYTHONPATH=/app/src
ENV HOME=/app

RUN ls -la /app/resources/

CMD ["python", "-m", "src.main"] 
