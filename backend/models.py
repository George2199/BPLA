from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    progress = db.Column(db.Float, default=0.0)
    
    themes = db.relationship('Theme', backref='course', lazy=True, cascade='all, delete-orphan')

class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    tasks = db.relationship('Task', backref='theme', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)  # video, test, etc.
    content = db.Column(JSON, nullable=True)  # вот это и есть "данные" задачи
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))
    status = db.Column(db.String, default='undone')  # waiting, passed, failed
    progress = db.Column(db.Float, default=0.0)
    
