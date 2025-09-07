from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Category(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(200))
    items       = db.relationship('Item', backref='category', lazy=True)

class Item(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(200))
    created_at  = db.Column(db.DateTime, server_default=db.func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def __repr__(self):
        return f'<Item {self.name}>'

class User(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    pw_hash  = db.Column(db.String(128), nullable=False)

    def set_password(self, pw):
        self.pw_hash = generate_password_hash(pw)
    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)