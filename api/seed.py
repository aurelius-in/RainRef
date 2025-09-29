from models.db import SessionLocal
from models.entities import User
from services.auth import hash_password


def upsert_admin() -> None:
    db = SessionLocal()
    try:
        email = "admin@rainref.local"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                id="u-admin",
                email=email,
                password_hash=hash_password("admin"),
                roles=["admin"],
                is_active=True,
            )
            db.add(user)
            db.commit()
            print("Seeded admin user: admin@rainref.local / admin")
        else:
            print("Admin user already exists")
    finally:
        db.close()


if __name__ == "__main__":
    upsert_admin()


