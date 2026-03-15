FROM python:3.11-slim

# 🔥 ВМИКАЄМО МИТТЄВІ ЛОГИ
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping
COPY . .
RUN chmod 777 .
RUN chmod 666 bank.db
EXPOSE 5000
CMD ["python", "app.py"]
