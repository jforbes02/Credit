from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
#creating Database for users, and passwords

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    credit_limit = db.Column(db.Integer, default=1000, nullable=False)
    current_balance = db.Column(db.Integer, default=0, nullable=False)
    account_status = db.Column(db.String(20), default='active')
    password = db.Column(db.String(80), nullable=False)
    items = db.relationship('Item', secondary='u_items', backref=db.backref('owners', lazy='dynamic'))
    #password protection
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def remove(self):
        db.session.delete(self)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False) #payement,cred^,purchase
    description = db.Column(db.String(255), nullable=False) #context
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='transaction', lazy='select')
    def __repr__(self):
        return f'<Transaction {self.id}: {self.transaction_type} ${self.amount}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self): #debugging
        return f'<Item {self.id}: {self.name}>'

u_items = db.Table('u_items',
                   db.Column('id', db.Integer, primary_key=True),
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                   db.Column('item_id', db.Integer, db.ForeignKey('item.id'), nullable=False),
                   db.Column('purchase_time', db.DateTime, nullable=False, default=datetime.utcnow))