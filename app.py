from flask import Flask, request, render_template, redirect, url_for, send_file
import psycopg2
from io import BytesIO
import pytz
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

# Метрики Prometheus
REQUEST_COUNT = Counter("flask_app_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("flask_app_request_latency_seconds", "Latency of HTTP requests", ["method", "endpoint", "http_status"])

# Подключение к базе данных
def get_db_connection():
    return psycopg2.connect(
        host="postgres",
        database="mydatabase",
        user="user",
        password="password"
    )

# Создание таблицы, если она еще не существует
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                image BYTEA,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        conn.commit()

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    # Увеличиваем счётчик запросов для всех путей
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()

    # Метрики задержки только для '/' и '/metrics'
    if request.path in ["/", "/metrics"]:
        request_latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.method, request.path, response.status_code).observe(request_latency)

    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        image = request.files.get("image")

        if content:
            image_data = None
            if image:
                image_data = image.read()

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO posts (content, image) VALUES (%s, %s);", (content, image_data))
                    conn.commit()

            return redirect(url_for("index"))

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, content, image, created_at FROM posts ORDER BY id DESC;")
            posts = cursor.fetchall()

    timezone = pytz.timezone("Asia/Yekaterinburg")
    posts_with_time = []
    for post in posts:
        post_time = post[3].astimezone(timezone).strftime('%Y-%m-%d %H:%M:%S')
        posts_with_time.append(post[:3] + (post_time,))

    return render_template("index.html", posts=posts_with_time)

@app.route("/image/<int:post_id>")
def image(post_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT image FROM posts WHERE id = %s;", (post_id,))
            image_data = cursor.fetchone()

    if image_data:
        return send_file(BytesIO(image_data[0]), mimetype='image/jpeg')

    return "Image not found", 404

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
