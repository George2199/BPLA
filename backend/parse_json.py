import json
with open(r"/home/nout/vue/BPLA_main/backend/data/tests/seed.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

for q in test_data["questions"]:
    for opt in q["options"]:
        print(q["options"][opt]["is_right"])
        # is_correct = bool(opt["is_right"])
        # db.session.add(Option(question_id=question.id, option_text=opt, is_right=is_correct))