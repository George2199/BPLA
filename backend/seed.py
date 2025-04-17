from models import db, Role, Theme, Task, Course
from app import app
import json

IMG_PATH = "/data/imgs/"
VIDEO_PATH = "/data/videos/"

def clear_tables():
    with app.app_context():
        print("⚠️ Удаление всех данных из таблиц...")

        # Удаляем сначала зависимые (Task → Theme → Course)
        Task.query.delete()
        Theme.query.delete()
        Course.query.delete()
        Role.query.delete()

        db.session.commit()
        print("✅ Все данные удалены.")

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
            image_url=IMG_PATH+"Python.png",
            progress=0.3
        )

        cosmos_course = Course(
            title="Аэрокосмос",
            image_url=IMG_PATH+"Cosmos.png",
            progress=0.0
        )

        drone_course = Course(
            title="Управление БПЛА",
            image_url=IMG_PATH+"Drone.png",
            progress=0.7
        )

        # Темы только для Python пока
        python_course.themes = [
            Theme(title="Тема 1: Основы синтаксиса", tasks=[
                Task(title="Видео: Переменные", type="video"),
                Task(title="Практика: Примитивы", type="practical")
            ]),
            Theme(title="Тема 2: Условия", tasks=[
Task(title="Видео: if/else", type="video", content=VIDEO_PATH + "narezka_1920x1080.mp4"),
                Task(
                    title="Тест 1: Контроллер и полёт",
                    type="test",
                    content=json.dumps({
                        "questions": [
                            {
                                "question": "Что такое БВС?",
                                "options": [
                                    "Беспилотное воздушное средство",
                                    "Беспилотное водное средство",
                                    "Беспилотное ветряное средство",
                                    "Беспилотное вкусное средство"
                                ]
                            },
                            {
                                "question": "Где нельзя запускать БВС?",
                                "options": [
                                    "Над военными объектами",
                                    "Вблизи аэропортов",
                                    "В закрытых помещениях",
                                    "На Юпитере"
                                ]
                            }
                        ]
                    })
                ),
            ])
        ]

        db.session.add_all([python_course, cosmos_course, drone_course])
        db.session.commit()
        print("✅ Courses, themes, and tasks seeded.")



if __name__ == "__main__":
    clear_tables()
    seed_roles()
    seed_courses()
