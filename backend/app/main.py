from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import random

from .database import Base, engine, get_db
from . import models, schemas, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam API")

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/register", response_model=schemas.TokenOut)
def register(data: schemas.RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        name=data.name,
        email=data.email,
        password_hash=auth.hash_password(data.password)
    )
    db.add(user); db.commit()
    token = auth.create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/login", response_model=schemas.TokenOut)
def login(data: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not auth.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/exam/start", response_model=schemas.StartExamOut)
def start_exam(count: int = 10, db: Session = Depends(get_db), current=Depends(auth.get_current_user)):
    q_ids = [q.id for q in db.query(models.Question.id).all()]
    picked = random.sample(q_ids, k=min(count, len(q_ids)))
    questions = (
        db.query(models.Question).filter(models.Question.id.in_(picked)).all()
    )
    # Eager load options by accessing
    _ = [q.options for q in questions]

    attempt = models.ExamAttempt(user_id=current.id, score=0, total=len(questions))
    db.add(attempt); db.commit(); db.refresh(attempt)

    return {"attempt_id": attempt.id, "questions": questions}

@app.post("/exam/submit", response_model=schemas.ResultOut)
def submit_exam(payload: schemas.SubmitExamIn, db: Session = Depends(get_db), current=Depends(auth.get_current_user)):
    attempt = db.query(models.ExamAttempt).filter(models.ExamAttempt.id == payload.attempt_id).first()
    if not attempt: raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.user_id != current.id: raise HTTPException(status_code=403, detail="Not your attempt")

    score = 0
    for ans in payload.answers:
        # record answer
        ua = models.UserAnswer(
            attempt_id=attempt.id,
            question_id=ans.question_id,
            selected_option_id=ans.selected_option_id
        )
        db.add(ua)
        # evaluate
        is_correct = db.query(models.Option.is_correct)\
                       .filter(models.Option.id == ans.selected_option_id).scalar()
        if is_correct: score += 1

    attempt.score = score
    db.commit()
    return {"attempt_id": attempt.id, "score": score, "total": attempt.total}
