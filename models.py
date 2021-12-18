from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from __main__ import db


# user table
class student(db.Model,UserMixin):
     __tablename__ = 'students'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), unique=True, nullable=False)
     password = db.Column(db.String(80), unique=True, nullable=False)
     email = db.Column(db.String(120), unique=True, nullable=False)
     phone = db.Column(db.String(120), unique=True, nullable=False)
     gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'))
     country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
     level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
     faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
     spiciality_id = db.Column(db.Integer, db.ForeignKey('spiciality.id'))

     def get_id(self):
          return self.id


     def __repr__(self):
          return '<User %r>' % self.username



class gender(db.Model):
     __tablename__ = 'gender'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     users = db.relationship('student', backref='gen', lazy='dynamic')

class country(db.Model):
     __tablename__ = 'country'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     users = db.relationship('student', backref='cntry', lazy='dynamic')
class level(db.Model):
     __tablename__ = 'level'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     users = db.relationship('student', backref='levl', lazy='dynamic')
class faculty(db.Model):
     __tablename__ = 'faculty'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     users = db.relationship('student', backref='facult', lazy='dynamic')

class spiciality(db.Model):
     __tablename__ = 'spiciality'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     users = db.relationship('student', backref='spiciali', lazy='dynamic')


class service_category(db.Model):
     __tablename__ = 'service_category'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     service = db.relationship('service', backref='serca', lazy='dynamic')

class service(db.Model):
     __tablename__ = 'service'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     service_category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'))