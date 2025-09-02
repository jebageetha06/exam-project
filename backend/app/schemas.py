from pydantic import BaseModel, EmailStr
from typing import List, Optional

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class OptionOut(BaseModel):
    id: int
    text: str
    class Config: orm_mode = True

class QuestionOut(BaseModel):
    id: int
    text: str
    options: List[OptionOut]
    class Config: orm_mode = True

class StartExamOut(BaseModel):
    attempt_id: int
    questions: List[QuestionOut]

class SubmitAnswerIn(BaseModel):
    question_id: int
    selected_option_id: int

class SubmitExamIn(BaseModel):
    attempt_id: int
    answers: List[SubmitAnswerIn]

class ResultOut(BaseModel):
    attempt_id: int
    score: int
    total: int
