from models import db, Role, Theme, Task, Course
import json

IMG_PATH = "/data/imgs/"
VIDEO_PATH = "/data/videos/"
CONSPECT_PATH = "/data/conspects/"

def clear_tables():
    print("⚠️ Удаление всех данных из таблиц...")

    # Удаляем сначала зависимые (Task → Theme → Course)
    Task.query.delete()
    Theme.query.delete()
    Course.query.delete()
    Role.query.delete()

    db.session.commit()
    print("✅ Все данные удалены.")

def seed_roles():
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
    if Course.query.first():
        print("🔍 Courses already seeded.")
        return
    
    python_course = Course(
        title="Python. Введение",
        image_url=IMG_PATH + "Python.png",
        progress=0.3
    )

    cosmos_course = Course(
        title="Аэрокосмос",
        image_url=IMG_PATH + "Cosmos.png",
        progress=0.0
    )

    drone_course = Course(
        title="Управление БПЛА",
        image_url=IMG_PATH + "Drone.png",
        progress=0.7
    )

    python_course.themes = [
        Theme(title="Тема 1: Основы синтаксиса", tasks=[
            Task(title="Видео: Переменные", type="video", content=VIDEO_PATH + "perem.mp4"),
            Task(title="Конспект: Переменные", type="conspect", content=CONSPECT_PATH + "conspect1.md"),
        ]),
        Theme(title="Тема 2: Условия", tasks=[
            Task(title="Видео: if/else", type="video", content=VIDEO_PATH + "ifelse.mp4"),
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
                            ],
                            "correct_answers": [0]
                        },
                        {
                            "question": "Что такое БВС1?",
                            "options": [
                                "Беспилотное воздушное средство",
                                "Беспилотное водное средство",
                                "Беспилотное ветряное средство",
                                "Беспилотное вкусное средство"
                            ],
                            "correct_answers": [0]
                        },
                        {
                            "question": "Где нельзя запускать БВС?",
                            "options": [
                                "Над военными объектами",
                                "Вблизи аэропортов",
                                "В закрытых помещениях",
                                "На Юпитере"
                            ],
                            "correct_answers": [0, 2]
                        }
                    ]
                })
            ),
            Task(
                title="Блоки кода 1: Hello, World!",
                type="block",
                content=json.dumps({
                    "description": "Собери правильный порядок строк для вывода 'Hello, World!'",

                    "test_files": ["test_block1.py", "test_block1_extra.py"],

                    "blocks": [
                        { "content": "def main():", "type": "code" },
                        { "content": "print('Hello, World!')", "type": "code" },
                        { "content": "main()", "type": "code" },
                        {
                            "type": "container",
                            "label": "for i in range(5):",
                            "children": [
                                { "content": "    print(i)", "type": "code" }
                            ]
                        },
                        { "content": "print('Goodbye, World!')", "type": "code" }
                    ]
                })
            ),
        ])
    ]

    db.session.add_all([python_course, cosmos_course, drone_course])
    db.session.commit()
    print("✅ Courses, themes, and tasks seeded.")
