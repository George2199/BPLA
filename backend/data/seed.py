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

    with open("./data/tests/tests_1.json", "r", encoding="utf-8") as f:
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

    db.session.add(BlockTask(task_id=block_task.id))

    bt = BlockType(type="code")
    db.session.add(bt)
    db.session.flush()
    bt = BlockType(type="container")
    db.session.add(bt)
    db.session.flush()

    python_course.themes = [
        Theme(title="Тема 1: Основы синтаксиса", tasks=[
            Task(title="Видео: Переменные", type="video", path=VIDEO_PATH + "perem.mp4"),
            Task(title="Конспект: Переменные", type="conspect", content=CONSPECT_PATH + "conspect1.md"),
        ]),
        Theme(title="Тема 2: Условия", tasks=[
            Task(title="Видео: if/else", type="video", content=VIDEO_PATH + "ifelse.mp4"),
        ])
    ]

    db.session.add_all([python_course, cosmos_course, drone_course])
    db.session.commit()
    print("✅ Courses, themes, and tasks seeded.")

def parse_blocks(json_path):
    l = []
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)

        for b in parse_data["blocks"]:
            l.append([b['cat'], b['type']])
    return l

def get_types(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)

        types = set([i['type'] for i in parse_data["blocks"]])

    return types
           
def commit_blocks(json_path):
    parse_data = parse_blocks(json_path)
    block_types = {t: BlockType.query.filter_by(type=t).first()
                   for t in get_types(json_path)}
    for b in parse_data:
        db.session.add(Block(cat = b[0], type_id = block_types[b[1]]))
    db.session.commit()

def parse_tests(json_path, test_id):
    l = []
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)
        for q in parse_data["questions"]:
            question = Question(test_id=test_id, question_text=q["question_text"])
            # db.session.add(question)
            # db.session.flush()
            opts = []
            for opt in (q["options"]):
                is_correct = bool(q["options"][opt]["is_right"])
                opts.append(Option(question_id=question.id, option_text=opt, is_right=is_correct))
            l.append([question, opts])
    return l

def commit_tests(json_path, test_id):
    parsed_data = parse_tests(json_path, test_id)
    for q in parsed_data:
        db.session.add(q[0])
        db.session.add_all(q[1])
    db.session.commit()