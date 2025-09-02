from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from . import models

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    if db.query(models.Question).count() > 0:
        print("Already seeded"); return

    # Q1
    q1 = models.Question(text="What is the capital of France?")
    db.add(q1); db.flush()
    db.add_all([
        models.Option(question_id=q1.id, text="Paris", is_correct=True),
        models.Option(question_id=q1.id, text="Lyon", is_correct=False),
        models.Option(question_id=q1.id, text="Marseille", is_correct=False),
        models.Option(question_id=q1.id, text="Nice", is_correct=False),
    ])

    # Q2
    q2 = models.Question(text="2 + 2 = ?")
    db.add(q2); db.flush()
    db.add_all([
        models.Option(question_id=q2.id, text="3", is_correct=False),
        models.Option(question_id=q2.id, text="4", is_correct=True),
        models.Option(question_id=q2.id, text="5", is_correct=False),
        models.Option(question_id=q2.id, text="22", is_correct=False),
    ])

    db.commit(); db.close()
    print("Seeded questions.")

if __name__ == "__main__":
    seed()
