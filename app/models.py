from pydantic import BaseModel, Field


class QuizAnswers(BaseModel):
    job_id: str = Field(..., description="Selected job ID from Q1")
    q2: str = Field(..., pattern="^[ABCD]$")
    q3: str = Field(..., pattern="^[ABCD]$")
    q4: str = Field(..., pattern="^[ABCD]$")
    q5: str = Field(..., pattern="^[ABCD]$")
    q6: str = Field(..., pattern="^[ABCD]$")


class ScoreResult(BaseModel):
    total_score: int
    breakdown: list[int]
    risk_level: str
    risk_label_zh: str
    risk_label_en: str
    advice_zh: str
    advice_en: str
    job_name_zh: str
    job_name_en: str
