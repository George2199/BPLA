from models import db, Role
from app import app

def seed_roles():
    with app.app_context():
        if Role.query.first():
            print("🔍 Roles already seeded. Skipping.")
            return

        roles = [
            Role(role_name="Admin", login="admin", password="amdin"),
            Role(role_name="User", login="user", password="user"),
            Role(role_name="Operator", login="op", password="op"),
        ]

        db.session.bulk_save_objects(roles)
        db.session.commit()
        print("✅ Roles table seeded successfully.")

if __name__ == "__main__":
    seed_roles()
