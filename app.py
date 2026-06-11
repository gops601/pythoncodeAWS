from flask import Flask,render_template,request
import boto3
import pymysql

app = Flask(__name__)

bucket_name="student-photo-demo-gopu"

db=pymysql.connect(
host="RDS-ENDPOINT",
user="admin",
password="Password@123",
database="studentdb"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    name=request.form['name']
    email=request.form['email']
    course=request.form['course']

    photo=request.files['photo']

    s3=boto3.client('s3')

    s3.upload_fileobj(
        photo,
        bucket_name,
        photo.filename
    )

    photo_url=f"https://{bucket_name}.s3.amazonaws.com/{photo.filename}"

    cursor=db.cursor()

    sql="""
    INSERT INTO students
    (name,email,course,photo_url)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(
        sql,
        (name,email,course,photo_url)
    )

    db.commit()

    return "Student Registered Successfully"

if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )