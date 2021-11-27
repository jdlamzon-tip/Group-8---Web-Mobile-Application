from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import requests
from firebase import firebase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'concepciongerandoylamzonlacanilao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
conn = sqlite3.connect("D:\DevOps\midterm\index\database.db")
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



@app.route('/')
#@login_required
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():  
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    iname = form.email.data
    iuser = form.username.data
    ipass = form.password.data
    db = firebase.FirebaseApplication("https://devopsproject-1c164-default-rtdb.asia-southeast1.firebasedatabase.app")
    db.put(f'/accounts/{iuser}', "username", iuser)
    db.put(f'/accounts/{iuser}', "name", iname)
    db.put(f'/accounts/{iuser}', "password", ipass)

    
    return render_template('signup.html', form=form)

    
@app.route('/login', methods=['GET', 'POST'])
def login():  
    form = LoginForm()
    
    
    if form.validate_on_submit():
        username = form.username.data
        parsed_data = requests.get(f'https://devopsproject-1c164-default-rtdb.asia-southeast1.firebasedatabase.app/accounts/{username}.json').json() 
        userdata = parsed_data['username']
        passdata = parsed_data['password']
        if form.username.data == userdata:
            if form.password.data == passdata:
                return redirect(url_for('home'))
        return '<h1>Invalid username or password</h1>'
    
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
