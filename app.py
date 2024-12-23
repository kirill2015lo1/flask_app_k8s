from flask import Flask, request, render_template, redirect, url_for, send_file
import psycopg2
from io import BytesIO

app = Flask(__name__, 
            template_folder="templates",  
            static_folder="static")  

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
                image BYTEA
            );
        """)
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        image = request.files.get("image")

        if content:
            image_data = None
            if image:
                image_data = image.read()  # Считывание изображения в байтовый формат
            
            # Сохранение контента и изображения в базе данных
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO posts (content, image) VALUES (%s, %s);", (content, image_data))
                    conn.commit()

            return redirect(url_for("index"))

    # Получение всех постов с изображениями, сортировка по убыванию ID
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, content, image FROM posts ORDER BY id DESC;")
            posts = cursor.fetchall()

    return render_template("index.html", posts=posts)

@app.route("/image/<int:post_id>")
def image(post_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT image FROM posts WHERE id = %s;", (post_id,))
            image_data = cursor.fetchone()

    if image_data:
        # Возвращаем изображение как файл
        return send_file(BytesIO(image_data[0]), mimetype='image/jpeg')

    return "Image not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
