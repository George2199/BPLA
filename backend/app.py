from flask import Flask, jsonify, request
from flask import send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Role, Course, Theme, Task
from config import Config
import json


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

def parse_content(content):
    try:
        if isinstance(content, str) and content.strip().startswith('{'):
            return json.loads(content)
        return content
    except Exception as e:
        print(f"⚠️ Ошибка парсинга контента: {e}")
        return None

@app.route('/')
def hello_world():
    return 'Hello from Flask Backend!'

@app.route('/roles')
def get_roles():
    roles = Role.query.order_by(Role.id).all()
    return jsonify([
        {"id": r.id, "role_name": r.role_name, "login": r.login, "password": r.password}
        for r in roles
    ])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'login' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Missing login or password"}), 400

    login_attempt = data['login']
    password_attempt = data['password']
    user = Role.query.filter_by(login=login_attempt, password=password_attempt).first()

    if user:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([
        {
            "id": c.id,
            "title": c.title,
            "image_url": c.image_url,
            "progress": c.progress,
            "themes": [
                {
                    "id": t.id,
                    "title": t.title,
                    "tasks": [
                        {
                            "id": task.id,
                            "title": task.title,
                            "type": task.type,
                            "content": parse_content(task.content)
                        } for task in t.tasks
                    ]
                } for t in c.themes
            ]
        } for c in courses
    ])

    
@app.route('/courses/<int:id>', methods=['GET'])
def get_course_by_id(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Курс не найден'}), 404

    return jsonify({
        "id": course.id,
        "title": course.title,
        "image_url": course.image_url,
        "progress": course.progress,
        "themes": [
            {
                "id": t.id,
                "title": t.title,
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "type": task.type,
                        "content": parse_content(task.content),
                    } for task in t.tasks
                ]
            } for t in course.themes
        ]
    })


@app.route('/themes', methods=['GET'])
def get_themes():
    themes = Theme.query.all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "type": task.type
                } for task in t.tasks
            ]
        } for t in themes
    ])

@app.route('/data/imgs/<path:filename>')
def serve_course_image(filename):
    return send_from_directory('data/imgs', filename)

@app.route('/data/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('data/videos', filename)

if __name__ == '__main__':
    app.run(debug=True)
