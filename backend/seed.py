from models import db, Role, Theme, Task, Course
from app import app

def seed_roles():
    with app.app_context():
        if Role.query.first():
            print("🔍 Roles already seeded. Skipping.")
            return

        roles = [
            Role(role_name="Admin", login="admin", password="admin"),
            Role(role_name="User", login="user", password="user"),
            Role(role_name="Operator", login="op", password="op"),
        ]

        db.session.bulk_save_objects(roles)
        db.session.commit()
        print("✅ Roles table seeded successfully.")

def seed_courses():
    with app.app_context():
        if Course.query.first():
            print("🔍 Courses already seeded.")
            return

        python_course = Course(
            title="Python. Введение",
            image_url="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg",
            progress=0.3
        )

        cosmos_course = Course(
            title="Аэрокосмос",
            image_url="https://cdn.pixabay.com/photo/2011/12/14/12/11/rocket-launch-11049_960_720.jpg",
            progress=0.0
        )

        drone_course = Course(
            title="Управление БПЛА",
            image_url="https://cdn.pixabay.com/photo/2016/11/29/09/15/drone-1866742_960_720.jpg",
            progress=0.7
        )

        # Темы только для Python пока
        python_course.themes = [
            Theme(title="Тема 1: Основы синтаксиса", tasks=[
                Task(title="Видео: Переменные", type="video"),
                Task(title="Практика: Примитивы", type="practical")
            ]),
            Theme(title="Тема 2: Условия", tasks=[
                Task(title="Видео: if/else", type="video"),
                Task(title="Тест: Условия", type="test")
            ])
        ]

        db.session.add_all([python_course, cosmos_course, drone_course])
        db.session.commit()
        print("✅ Courses, themes, and tasks seeded.")



if __name__ == "__main__":
    seed_roles()
    seed_courses()
