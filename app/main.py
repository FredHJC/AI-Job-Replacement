from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import TEMPLATES_DIR, STATIC_DIR
from app.data.jobs import JOBS, JOB_GROUPS, OVERRIDE_JOBS, CONSISTENCY_WARNINGS
from app.data.questions import QUESTIONS
from app.data.explanations import DIMENSION_EXPLANATIONS
from app.scoring import compute_result
from app.models import QuizAnswers
from app.db import init_db, save_submission, get_submission

app = FastAPI(title="Will AI Replace My Job?")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Make tojson output raw UTF-8 instead of \uXXXX escapes
templates.env.policies["json.dumps_kwargs"] = {"ensure_ascii": False}

init_db()


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
            "override_jobs": list(OVERRIDE_JOBS.keys()),
            "consistency_warnings": CONSISTENCY_WARNINGS,
        },
    )


@app.post("/api/score")
async def score(answers: QuizAnswers):
    result = compute_result(answers)
    result_dict = result.model_dump()

    sid = save_submission(
        job_id=answers.job_id,
        answers={"q2": answers.q2, "q3": answers.q3, "q4": answers.q4, "q5": answers.q5, "q6": answers.q6},
        result=result_dict,
    )

    return {**result_dict, "result_id": sid}


@app.get("/result/{result_id}", response_class=HTMLResponse)
async def result_by_id(request: Request, result_id: str):
    submission = get_submission(result_id)
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "explanations": DIMENSION_EXPLANATIONS,
            "server_result": submission["result"] if submission else None,
        },
    )


@app.get("/result", response_class=HTMLResponse)
async def result(request: Request):
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "explanations": DIMENSION_EXPLANATIONS,
            "server_result": None,
        },
    )
