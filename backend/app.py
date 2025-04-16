from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Role
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

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

if __name__ == '__main__':
    app.run(debug=True)
