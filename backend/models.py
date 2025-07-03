from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    save_block = db.relationship('SaveBlock')
    save_test = db.relationship('SaveTest')

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
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type_id = db.Column(db.Integer, db.ForeignKey('task_types.id'), nullable=False)
    content = db.Column(JSON, nullable=True)  # вот это и есть "данные" задачи
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))
    status = db.Column(db.String, default='undone')  # waiting, passed, failed
    progress = db.Column(db.Float, default=0.0)
    
class TaskType(db.Model):
    __tablename__ = 'task_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    tasks = db.relationship('Task', backref='task_type', lazy=True)

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    path = db.Column(db.String, nullable=False)

class Conspect(db.Model):
    __tablename__ = 'conspects'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    path = db.Column(db.String, nullable=False)

    files = db.relationship('File', backref='conspect', lazy=True, cascade='all, delete-orphan')

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    conspect_id = db.Column(db.Integer, db.ForeignKey('conspects.id'), nullable=False)
    file_path = db.Column(db.String, nullable=False)

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    questions = db.relationship('Question', backref='test', lazy=True, cascade='all, delete-orphan')
    save_test = db.relationship('SaveTest')

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_text = db.Column(db.String, nullable=False)

    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')
    save_test = db.relationship('SaveTest')

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_text = db.Column(db.String, nullable=False)
    is_right = db.Column(db.Boolean, default=False)

    save_test = db.relationship('SaveTest')
    
class BlockType(db.Model):
    __tablename__ = 'block_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False, unique=True)  # unique для удобства поиска

    blocks = db.relationship('Block', backref='block_type', lazy=True)

class Block(db.Model):
    __tablename__ = 'blocks'
    id = db.Column(db.Integer, primary_key=True)
    block_task_id = db.Column(db.Integer, db.ForeignKey('block_tasks.id'), nullable=True)
    cat = db.Column(db.String)

    type_id = db.Column(db.Integer, db.ForeignKey('block_types.id'), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('blocks.id'), nullable=True)
    save_block = db.relationship('SaveBlock')

class BlockTask(db.Model):
    __tablename__ = 'block_tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    task = db.relationship('Task')
    save_blocks = db.relationship('SaveBlock', backref='block', lazy=True)
    blocks = db.relationship('Block', backref='block_task', lazy=True)

class SaveBlock(db.Model):
    __tablename__ = 'save_blocks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    block_task_id = db.Column(db.Integer, db.ForeignKey('block_tasks.id'), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.id'), nullable=False)

    is_used = db.Column(db.Boolean, nullable=True)
    place = db.Column(db.Integer, nullable=True)
    parent = db.Column(db.Integer, nullable=True)

class SaveTest(db.Model):
    __tablename__ = 'save_tests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=False)

    option_state = db.Column(db.Boolean, nullable=True)