from models.db import SessionLocal
from models.entities import User, KbCard
from services.auth import hash_password
from services.kb_embed import embed_text


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


def seed_kb_minimal() -> None:
    db = SessionLocal()
    try:
        count = db.query(KbCard).count()
        if count == 0:
            body = (
                "If a user did not get the activation email, resend the activation link. "
                "Ensure the user's email is correct and not blocked."
            )
            card = KbCard(
                id="kb-activation",
                title="Activation troubleshooting",
                body=body,
                tags=["activation", "support"],
                embedding=embed_text(body),
            )
            db.add(card)
            db.commit()
            print("Seeded minimal KB card: Activation troubleshooting")
        else:
            print(f"KB already has {count} cards")
    finally:
        db.close()


if __name__ == "__main__":
    upsert_admin()
    seed_kb_minimal()


