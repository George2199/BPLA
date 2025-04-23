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
        ],
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

@app.route('/submit_test', methods=['POST'])
def submit_test():
    import json

    data = request.get_json()
    answers = data.get('answers')
    task_id = data.get('task_id')

    task = Task.query.get(task_id)
    if not task or task.type != 'test':
        return jsonify({"success": False, "message": "Неверный task_id"}), 400

    # Парсим контент
    content = task.content
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            return jsonify({"success": False, "message": "Невозможно прочитать контент теста"}), 500

    questions = content.get("questions", [])
    if len(answers) != len(questions):
        return jsonify({"success": False, "message": "Ответов должно быть столько же, сколько вопросов"}), 400

    correct_count = 0
    details = []

    for i, question in enumerate(questions):
        correct_answers = set(map(int, question.get("correct_answers", [])))
        user_answers = set(map(int, answers[i])) if isinstance(answers[i], list) else set()

        is_correct = user_answers == correct_answers
        print('usr:', user_answers, 'corr:', correct_answers)
        if is_correct:
            correct_count += 1

        details.append({
            "question": question.get("question", "???"),
            "is_correct": is_correct,
            "your": sorted(list(user_answers)),
            "correct": sorted(list(correct_answers))
        })

    # Сохраняем статус
    score_ratio = correct_count / len(questions)
    task.status = 'passed' if score_ratio >= 0.7 else 'failed'
    task.progress = score_ratio
    db.session.commit()

    return jsonify({
        "success": True,
        "score": correct_count,
        "total": len(questions),
        "details": details
    })

if __name__ == '__main__':
    app.run(debug=True)
