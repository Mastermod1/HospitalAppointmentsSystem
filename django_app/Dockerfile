FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN chmod +x /app/scripts/wait_for_it.sh
RUN chmod +x /app/scripts/start.sh

CMD ["sh", "/app/scripts/start.sh"]
