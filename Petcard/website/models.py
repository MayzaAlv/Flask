from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    data_created = db.Column(db.DateTime(timezone=True), default=func.now()) 
    pet = db.relationship('Petcard', backref='user', passive_deletes=  True)


class Petcard(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.String(100))
    birthday = db.Column(db.Date) 
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(1))
    owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    