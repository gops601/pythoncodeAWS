
import os
from flask import Flask, render_template, request
import boto3
import pymysql

app = Flask(__name__)

bucket_name = os.environ["S3_BUCKET_NAME"]

db_config = {
    "host": os.environ["DB_HOST"],
    "port": 3306,
    "user": os.environ.get("DB_USER", "admin"),
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ.get("DB_NAME", "studentdb")
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():

    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    photo = request.files['photo']

    if not photo or not photo.filename:
        return "Please select a student photo.", 400

    s3 = boto3.client('s3')

    photo_name = photo.filename
    s3.upload_fileobj(
        photo,
        bucket_name,
        photo_name
    )

    photo_url = (
        f"https://{bucket_name}.s3.amazonaws.com/{photo_name}"
    )

    connection = None

    try:
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            sql = """
            INSERT INTO students
            (name, email, course, photo_url)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (name, email, course, photo_url)
            )

        connection.commit()

        return "Student Registered Successfully"

    except Exception:
        if connection:
            connection.rollback()

        app.logger.exception("Student registration failed")
        return "Registration failed. Check the application logs.", 500

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
