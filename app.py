from flask import Flask, render_template, redirect, flash, url_for, request, session
from flask_login import LoginManager, logout_user, login_required, current_user, LoginManager, login_user
from livereload import Server
from tornado.web import authenticated
from werkzeug.security import generate_password_hash

from database import db, User, Config, Transaction

"""
App that
1. Creates profile for users
2. Provides new users a credit line based on age
3. Has the user play rock-paper-scissors in order to pay back "credit"
4. Allow users to buy things with credit
5. Gives penalty to people that go over the credit limit

"""
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "secreter"
db.init_app(app)

#Login
login_manager = LoginManager()  #creates authentication system
login_manager.init_app(app)  #integrates login system with flask
login_manager.login_view = 'login'  #tells flask go to login page for unauthorized users


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/registration', methods=['GET', 'POST'])
def register():
    """
    Handles registration forms and sends new user info into the database
    """
    if request.method == 'POST':
        username = request.form['username'] #form data
        email = request.form['email'] #form data
        password = request.form['password'] #form data
        age = request.form['age']
        #one email per username
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        hashed_pass = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pass, age=age)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template("registration.html")


@login_manager.user_loader
def load_user(user_id):
    """
    #logged in users stay logged in when going to different page
    :param user_id: ID of the user to load
    :return: User object
    """
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """" Handles logging into the website from form submissions """
    if request.method == 'POST':
        email = request.form['email']  #form data
        password = request.form['password']  #form data

        user = User.query.filter_by(email=email).first()  #looks in database for user with email

        if user and user.check_password(password):  #checks if user was found and if password is valid
            login_user(user)  #creates session and authenticates user
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        elif not user:
            flash('User does not exist')
            return redirect(url_for('login'))
        else:
            flash('Incorrect password')
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

with app.app_context():
    #db.drop_all()
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
