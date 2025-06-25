from models import db, BlockType, Role, Course, Theme, Task, TaskType, Video, Conspect, File, Test, Question, Option, Block, BlockTask
import json

IMG_PATH = "/data/imgs/"
VIDEO_PATH = "/data/videos/"
CONSPECT_PATH = "/data/conspects/"

def clear_tables():
    print("⚠️ Удаление всех данных из таблиц...")

    # Удаляем сначала зависимые (Task → Theme → Course)
    Option.query.delete()
    Question.query.delete()
    Test.query.delete()
    File.query.delete()
    Conspect.query.delete()
    Video.query.delete()
    BlockTask.query.delete()
    Block.query.delete()
    Task.query.delete()
    TaskType.query.delete()
    Theme.query.delete()
    Course.query.delete()
    Role.query.delete()
    BlockType.query.delete()
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

    theme1 = Theme(course_id = python_course.id, title="Тема 1: Основы синтаксиса")
    theme2 = Theme(course_id = python_course.id, title="Тема 2: Условия")

    # Видео задача
    video_task = Task(title="Видео: Переменные", type="video", theme_id = theme1.id)
    db.session.add(video_task)
    db.session.flush()
    db.session.add(Video(task_id=video_task.id, path=VIDEO_PATH + "perem.mp4"))

    conspect_task = Task(title="Конспект: Переменные", type="conspect", theme_id = theme1.id)
    db.session.add(conspect_task)
    db.session.flush()
    conspect = Conspect(task_id=conspect_task.id, path=CONSPECT_PATH + "conspect1.md")
    db.session.add(conspect)
    db.session.flush()
    db.session.add(File(conspect_id=conspect.id, file_path=CONSPECT_PATH + "conspect1.md"))

    video_task = Task(title="Видео: if/else", type="video", theme_id = theme2.id)
    db.session.add(video_task)
    db.session.flush()
    db.session.add(Video(task_id=video_task.id, path=VIDEO_PATH + "ifelse.mp4"))

    test_task = Task(title="Тест 1: Контроллер и полёт", type="test", theme_id = theme2.id)
    db.session.add(test_task)
    db.session.flush()
    test = Test(task_id=test_task.id)
    db.session.add(test)
    db.session.flush()

    with open("./data/tests/seed.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    for q in test_data["questions"]:
        question = Question(test_id=test.id, question_text=q["question_text"])
        db.session.add(question)
        db.session.flush()
        for opt in (q["options"]):
            is_correct = bool(q["options"][opt]["is_right"])
            db.session.add(Option(question_id=question.id, option_text=opt, is_right=is_correct))

    block_task = Task(title="еБлоки кода 1: Hello, World!", type="block", theme_id = theme2.id)
    db.session.add(block_task)
    db.session.flush()

    db.session.add(BlockTask(task_id=block_task.id, block_id=block.id))

    bt = BlockType(type="code")
    db.session.add(bt)
    db.session.flush()
    bt = BlockType(type="container")
    db.session.add(bt)
    db.session.flush()

    blocks = [
        Block(cat="def main()", type=BlockType.query.filter_by(type="code").first()),
        Block(cat="print('Hello, World!", type=BlockType.query.filter_by(type="code").first()),
        Block(cat="main()", type= BlockType.query.filter_by(type="code").first()),
        Block(cat="for i in range(5):", type = BlockType.query.filter_by(type="container").first()),
        Block(cat="basic", type = BlockType.query.filter_by(type="code").first()),
    ]

    for block in blocks:
        db.session.add(block)
        db.session.flush()

    python_course.themes = [
        Theme(title="Тема 1: Основы синтаксиса", tasks=[
            Task(title="Видео: Переменные", type="video", path=VIDEO_PATH + "perem.mp4"),
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
