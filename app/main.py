from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import TEMPLATES_DIR, STATIC_DIR
from app.data.jobs import JOBS, JOB_GROUPS
from app.data.questions import QUESTIONS
from app.scoring import compute_result
from app.models import QuizAnswers

app = FastAPI(title="Will AI Replace My Job?")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/questionnaire", response_class=HTMLResponse)
async def questionnaire(request: Request):
    return templates.TemplateResponse(
        request,
        "questionnaire.html",
        {
            "jobs": JOBS,
            "job_groups": JOB_GROUPS,
            "questions": QUESTIONS,
        },
    )


@app.post("/api/score")
async def score(answers: QuizAnswers):
    result = compute_result(answers)
    return result


@app.get("/result", response_class=HTMLResponse)
async def result(request: Request):
    return templates.TemplateResponse(request, "result.html")
