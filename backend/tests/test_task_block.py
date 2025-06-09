import os
import sys
import unittest

# Ensure backend module path
CURRENT_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
sys.path.append(BACKEND_DIR)

from app import app
from models import db, Task

class ExecuteBlockEndpointTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()
            try:
                import seed
                seed.clear_tables()
                seed.seed_roles()
                seed.seed_courses()
            except Exception:
                pass

    def test_execute_block_correct_code(self):
        with self.app.app_context():
            task = Task.query.filter_by(title="Блоки кода 1: Hello, World!").first()
            self.assertIsNotNone(task, "Seeded block task not found")

        code = """\
def main():
    print('Hello, World!')
    for i in range(5):
        print(i)
    print('Goodbye, World!')

main()
"""
        resp = self.client.post('/execute', json={'code': code, 'task_id': task.id})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        self.assertIn('Hello, World!', data.get('output'))

if __name__ == '__main__':
    unittest.main()
