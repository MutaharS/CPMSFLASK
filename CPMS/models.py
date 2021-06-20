from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    uid = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    def get_id(self):
        return self.uid

class Admin(UserMixin, db.Model):
    aid = db.Column(db.Integer, primary_key=True) # FK -> aid connects to uid
    user = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    def get_id(self):
        return self.aid
    
class Paper(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    author = db.Column(db.String(100))
    papername = db.Column(db.String(100))
    paperpath = db.Column(db.String(100))
    subtime = db.Column(db.String(100))

    # Primary key
    def get_id(self):
        return self.pid