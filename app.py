from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql

app=Flask(__name__)

users={'user1': {'username': 'user1', 'password': 'pass1'},
       'user2': {'username': 'user2', 'password': 'pass2'}}

@app.route('/')

def dashboard():
    return render_template('dashboard.html')

@app.route('/index')
def index():
   con=sql.connect("db_web.db")
   con.row_factory=sql.Row
   cur=con.cursor()
   cur.execute("SELECT * from users")
   data=cur.fetchall()
   return render_template('index.html',datas=data)
  


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user=users.get(username)
        con=sql.connect("db_web.db")
        cur=con.cursor()
        cur.execute("insert into users(USERNAME,PASSWORD) values(?,?)",(username,password))
        con.commit()
        flash('USER ADDED','success')
        return redirect(url_for("index"))

        if user and user['password'] == password:
            return f'welcome,{username}!'
        else:
            return 'Invalid username or password. please try again.'
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return 'Username already exist'
        
        else:
            users[username] = {'username':username,'password':password}
            return 'Registration Successfully!!'
    return render_template('register.html')
if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)