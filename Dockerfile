# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /flask_app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Открываем порт 5000 для Flask
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]
