from flask import Flask, render_template
from flask_login import LoginManager
from livereload import Server
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
db.init_app(app)
with app.app_context():
    db.create_all()
#class UserForm(Form):
@app.route('/') #when they go to root of website
def index():
    return "drink"

@app.route('/registration')
def register():
    return render_template("registration.html")
if __name__ == '__main__':
    app.run(debug=True)