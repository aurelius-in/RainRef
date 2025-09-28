import os
import sys

print("Seeding minimal KB cards, tickets, signals, and an example event...")

SQL = """
CREATE EXTENSION IF NOT EXISTS vector;
INSERT INTO kb_cards (id, title, body, tags) VALUES
  ('kb-activation', 'Account activation', 'Steps to resend activation and troubleshoot email issues.', '{support,activation}')
ON CONFLICT (id) DO NOTHING;

INSERT INTO ref_events (id, source, channel, text) VALUES
  ('e-seed1','email','support','I did not get the activation email')
ON CONFLICT (id) DO NOTHING;

INSERT INTO product_signals (id, origin, type, strength, evidence_refs) VALUES
  ('s-seed1','ticket:t1','friction',0.8,'{"kb:activation"}')
ON CONFLICT (id) DO NOTHING;

INSERT INTO tickets (id, status) VALUES ('t-seed1','open') ON CONFLICT (id) DO NOTHING;
"""

def main():
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rainref")
    print(f"Target DB: {db_url}")
    try:
        import psycopg
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(SQL)
                conn.commit()
        print("Seeded core records.")
    except Exception as e:
        print("Seed skipped (install psycopg or ensure DB is up):", e)
        sys.exit(0)

if __name__ == "__main__":
    main()
