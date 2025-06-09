import os
import sys
import json
import unittest

# Ensure backend module path
CURRENT_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
sys.path.append(BACKEND_DIR)

from app import app
from models import db, Task

class SubmitTestEndpointTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    def test_submit_test_correct_answers(self):
        with self.app.app_context():
            task = Task.query.filter_by(title="Тест 1: Контроллер и полёт").first()
            self.assertIsNotNone(task, "Seeded test task not found")

            content = task.content
            if isinstance(content, str):
                content = json.loads(content)

            questions = content.get("questions", [])
            answers = [q.get("correct_answers", []) for q in questions]
        resp = self.client.post('/submit_test', json={'answers': answers, 'task_id': task.id})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(data.get('score'), len(questions))
        self.assertAlmostEqual(data.get('progress'), 1.0)

if __name__ == '__main__':
    unittest.main()
