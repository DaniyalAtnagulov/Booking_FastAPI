FROM python:3.12.0-slim

# Обновляем пакеты и устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /booking

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/booking

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Даём права на выполнение shell-скриптам (предполагается, что скрипты в /booking/docker/)
RUN chmod +x /booking/docker/*.sh

# Открываем порт для приложения
EXPOSE 8000

# Команда запуска по умолчанию (Gunicorn с Uvicorn worker)
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
