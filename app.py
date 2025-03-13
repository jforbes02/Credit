from flask import Flask, render_template, redirect, flash, url_for, request, session
from flask_login import LoginManager, logout_user, login_required, current_user
from livereload import Server
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
app.secret_key="secreter"
db.init_app(app)

#class UserForm(Form):
@app.route('/') #when they go to root of website
def index():
    return "drink "

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))

with app.app_context():
    db.drop_all()
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)