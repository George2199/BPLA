import json
import os
from flask import Flask
from flask_migrate import upgrade, Migrate
from config import BaseConfig
from models import db, BlockType, Role, Course, Theme, Task, TaskType, Video, Conspect, File, Test, Question, Option, Block, BlockTask

IMG_PATH = "/data/imgs/"
VIDEO_PATH = "/data/videos/"
CONSPECT_PATH = "/data/conspects/"

def run_migrations():
    print("📦 Running migrations...")

    from flask import Flask
    from flask_migrate import upgrade, Migrate
    from models import db
    from config import BaseConfig

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = BaseConfig.get_sqlite_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        upgrade()

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

    with open("./data/courses.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        gpt_seed_from_json(data)

def parse_courses(courses_path):
    l = []

    with open(courses_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)

        for c in parse_data["courses"]:
            course_id = commit_course_and_get_id()
            parse_tasks(f)


def commit_types(json_path):
    l = []
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)

        for b in parse_data["blocks"]:
            l.append([b['cat'], b['type']])
    return l

def parse_blocks(json_path):
    l = []
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)

        for b in parse_data["blocks"]:
            l.append([b['cat'], b['type']])
    return l

def parse_tasks(json_path):
    l = []
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)

        for t in parse_data["tasks"]:
            l.append([t['cat'], t['type']])
    return l

def get_types(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)

        types = set([i['type'] for i in parse_data["blocks"]])

    return types
           
def commit_blocks(blocks, types):
    parse_data = blocks
    block_types = {t: BlockType.query.filter_by(type=t).first()
                   for t in types}
    for b in parse_data:
        db.session.add(Block(cat = b[0], type_id = block_types[b[1]]))
    db.session.commit()

def parse_tests(json_path, task_id):
    l = []
    with open(json_path, "r", encoding="utf-8") as f:
        parse_data = json.load(f)
        for q in parse_data["questions"]:
            question_id = commit_question_and_get_id(test_id=commit_test_and_get_id(task_id),
                                       question_text=q["question_text"])
            opts = []
            for opt in (q["options"]):
                is_correct = bool(q["options"][opt]["is_right"])
                opts.append(Option(question_id=question_id, option_text=opt, is_right=is_correct))
            l.append(opts)
    return l


def commit_course_and_get_id(test_id, question_text) -> int:
    question = Question(test_id=test_id, question_text=question_text)
    db.session.add(question)
    db.session.commit()

def commit_question_and_get_id(test_id, question_text) -> int:
    question = Question(test_id=test_id, question_text=question_text)
    db.session.add(question)
    db.session.commit()

    return question.id

def commit_test_and_get_id(task_id) -> int:
    # task
    test = Test(task_id=task_id)
    db.session.add(test)
    db.session.commit()

    return test.id

def commit_opts(opts):
    parsed_data = opts
    for q in parsed_data:
        db.session.add_all(q)
    db.session.commit()

def gpt_seed_from_json(data):
    for course_key, course_data in data["courses"].items():
        course = Course(
            title=course_data["title"],
            image_url=IMG_PATH + course_data.get("image", ""),
            progress=course_data.get("progress", 0.0)
        )
        db.session.add(course)
        db.session.flush()

        for theme_title, theme_data in course_data.get("themes", {}).items():
            theme = Theme(title=theme_title, course_id=course.id)
            db.session.add(theme)
            db.session.flush()

            for task_title, task_data in theme_data["tasks"].items():
                print(task_title)
                task_type = get_or_create_task_type(task_data["type"])
                task = Task(title=task_title, type_id=task_type.id, theme_id=theme.id)
                db.session.add(task)
                db.session.flush()

                match task_data["type"]:
                    case "video":
                        db.session.add(Video(task_id=task.id, path=VIDEO_PATH + task_data["video"]))
                    case "conspect":
                        conspect = Conspect(task_id=task.id, path=CONSPECT_PATH + task_data["conspect"])
                        db.session.add(conspect)
                        db.session.flush()
                        for f in task_data.get("files", []):
                            db.session.add(File(conspect_id=conspect.id, file_path=CONSPECT_PATH + f))
                    case "test":
                        test = Test(task_id=task.id)
                        db.session.add(test)
                        db.session.flush()
                        for q in task_data["questions"]:
                            question = Question(test_id=test.id, question_text=q["question_text"])
                            db.session.add(question)
                            db.session.flush()
                            for option_text, option_data in q["options"].items():
                                db.session.add(Option(
                                    question_id=question.id,
                                    option_text=option_text,
                                    is_right=bool(option_data["is_right"])
                                ))
                    case "blocks":
                        block_task = BlockTask(task_id=task.id)
                        db.session.add(block_task)
                        db.session.flush()
                        for b in task_data["blocks"]:
                            block_type = BlockType.query.filter_by(type=b["type"]).first()
                            if not block_type:
                                block_type = BlockType(type=b["type"])
                                db.session.add(block_type)
                                db.session.flush()
                            db.session.add(Block(cat=b["cat"], type_id=block_type.id, block_task_id=block_task.id))

    db.session.commit()
    print("✅ JSON import complete.")

def get_or_create_task_type(name):
    tt = TaskType.query.filter_by(type=name).first()
    if not tt:
        tt = TaskType(type=name)
        db.session.add(tt)
        db.session.flush()
    return tt
