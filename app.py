from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route("/")
def main():
    # return "Welcome!"
    return render_template('index.html')


@app.route('/signUp',methods = ['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
    data = cursor.fetchall()

    if len(data) is 0:
        # Note: The following line must be added to commit changes into database. Then use 1. mysql -u root -p
        # 2. SELECT * FROM BucketList.tbl_user to check the database content
        conn.commit()
        return json.dumps({'html':'<span> All fields good !!</span>'})
    else:
        return json.dumps({'error':str(data[0])})


@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run()