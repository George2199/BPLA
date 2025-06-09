from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Role, Course, Theme, Task
from config import BaseConfig
import json, io, contextlib, sys, os, types, unittest

# Определяем пути
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
db_path = os.path.join(DATA_DIR, 'app.db')

# Создаем Flask app
app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config["SQLALCHEMY_DATABASE_URI"] = BaseConfig.get_sqlite_uri(db_path)

# Инициализация
db.init_app(app)
migrate = Migrate(app, db)


with open("db_debug_path.log", "w", encoding="utf-8") as f:
    f.write(f"[DEBUG] DB WILL BE LOADED FROM: {db_path}\n")

if not os.path.exists(db_path):
    print("[INFO] Database not found. Initializing...")

    with app.app_context():
        db.create_all()
        try:
            import seed
            seed.clear_tables()
            seed.seed_roles()
            seed.seed_courses()
            print("[INFO] Initialization complete.")
        except Exception as e:
            print(f"[ERROR] Initialization failed: {e}")

CORS(app, resources={r"/*": {"origins": "*"}})

def parse_content(content):
    try:
        if isinstance(content, str) and content.strip().startswith('{'):
            return json.loads(content)
        return content
    except Exception as e:
        print(f"⚠️ Ошибка парсинга контента: {e}")
        return None
    
def update_course_progress(course_id):
    course = Course.query.get(course_id)
    if not course:
        return

    test_tasks = Task.query.join(Theme).filter(
        Theme.course_id == course.id,
        Task.type == 'test'
    ).all()

    if not test_tasks:
        course.progress = 0.0
    else:
        total = len(test_tasks)
        passed = sum(task.progress for task in test_tasks)
        course.progress = passed / total

    db.session.commit()

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
    courses = Course.query.order_by(Course.id).all()
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
    return send_from_directory(os.path.join(DATA_DIR, 'imgs'), filename)

@app.route('/data/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(os.path.join(DATA_DIR, 'videos'), filename)

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

    theme = Theme.query.get(task.theme_id)
    if theme:
     course = Course.query.get(theme.course_id)
    if course:
        # Пересчитать средний прогресс по всем таскам в курсе
        all_tasks = Task.query.join(Theme).filter(Theme.course_id == course.id).all()
        if all_tasks:
            avg_progress = sum(t.progress for t in all_tasks) / len(all_tasks)
            course.progress = avg_progress
            db.session.commit()


    update_course_progress(course.id)

    return jsonify({
        "success": True,
        "score": correct_count,
        "total": len(questions),
        "progress": task.progress,
        "details": details
    })

@app.route('/data/conspects/<path:filename>')
def serve_conspect(filename):
    return send_from_directory(os.path.join(DATA_DIR, 'conspects'), filename, mimetype='text/markdown')

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')
    task_id = data.get('task_id')

    stdout_capture = io.StringIO()
    exec_namespace = {}

    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(code, exec_namespace)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    user_output = stdout_capture.getvalue()

    if not task_id:
        return jsonify({'output': user_output})

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    content = task.content
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except Exception:
            content = {}

    test_files = content.get('test_files')
    if not test_files:
        single = content.get('test_file')
        test_files = [single] if single else []

    if not test_files:
        return jsonify({'output': user_output})

    all_output = io.StringIO()
    overall_success = True

    for fname in test_files:
        test_path = os.path.join(BASE_DIR, 'block_tests', fname)
        if not os.path.exists(test_path):
            return jsonify({'error': f'Test file {fname} not found'}), 500

        with open(test_path, 'r', encoding='utf-8') as f:
            test_code = f.read()

        test_module = types.ModuleType(f"test_module_{fname}")
        test_module.__dict__.update(exec_namespace)
        test_module.user_output = user_output
        exec(test_code, test_module.__dict__)

        suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)
        buffer = io.StringIO()
        result = unittest.TextTestRunner(stream=buffer, verbosity=2).run(suite)
        all_output.write(buffer.getvalue())
        if not result.wasSuccessful():
            overall_success = False

    return jsonify({
        'output': user_output,
        'tests_output': all_output.getvalue(),
        'success': overall_success

    })

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)