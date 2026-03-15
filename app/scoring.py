from app.data.jobs import JOBS_BY_ID, OVERRIDE_JOBS
from app.data.questions import QUESTIONS
from app.models import QuizAnswers, ScoreResult

OPTION_SCORES = {"A": 4, "B": 3, "C": 2, "D": 1}

RISK_LEVELS = [
    {
        "min": 20,
        "max": 24,
        "level": "extreme",
        "label_zh": "极高风险区",
        "label_en": "Extreme Risk Zone",
        "tag_zh": "自动化重灾区",
        "tag_en": "Automation Ground Zero",
        "advice_zh": (
            "您的工作高度集中在纯数字处理、遵循显性规则和基础执行层面。"
            "当前 AI 的能力已经可以直接覆盖您的大部分核心任务。\n\n"
            '建议：迫切需要向"复杂决策"、"人际协调"或"AI 管理者"的方向转型，'
            '将自己从"执行者"转变为"审查者"。'
        ),
        "advice_en": (
            "Your work is heavily concentrated in pure digital processing, "
            "following explicit rules, and basic execution. "
            "Current AI can already cover most of your core tasks.\n\n"
            "Advice: Urgently pivot toward complex decision-making, "
            "interpersonal coordination, or AI management roles — "
            "transition from 'executor' to 'reviewer.'"
        ),
    },
    {
        "min": 14,
        "max": 19,
        "level": "high",
        "label_zh": "中高风险区",
        "label_en": "Medium-High Risk Zone",
        "tag_zh": "人机重构与溢价区",
        "tag_en": "Human-AI Restructuring Zone",
        "advice_zh": (
            '您的工作正处于 AI 能力的"锯齿状前沿"上。'
            "AI 能极大提升您搜集资料和生成初稿的速度，但依然需要您的专业判断来兜底。\n\n"
            "建议：不要把工作完全外包给 AI，而是学会深度驾驭它。"
            "熟练使用 AI 工具的员工将有机会淘汰那些不使用 AI 的同行。"
        ),
        "advice_en": (
            "Your work sits on AI's 'jagged frontier.' "
            "AI can dramatically speed up your research and first drafts, "
            "but your professional judgment is still essential.\n\n"
            "Advice: Don't outsource everything to AI — learn to deeply harness it. "
            "Employees who master AI tools will outcompete those who don't."
        ),
    },
    {
        "min": 8,
        "max": 13,
        "level": "low",
        "label_zh": "较低风险区",
        "label_en": "Low Risk Zone",
        "tag_zh": "护城河稳固区",
        "tag_en": "Strong Moat Zone",
        "advice_zh": (
            '您的工作高度依赖无法被数字化的"隐性知识"、复杂的人际博弈、'
            "道德法律责任背书，或是物理空间的真实交互。\n\n"
            "建议：AI 目前对您来说只是一个提高边缘效率的办公软件。"
            "继续深耕您的行业人脉、领导力或专业动手技能，这些在未来将变得更加稀缺和昂贵。"
        ),
        "advice_en": (
            "Your work heavily depends on tacit knowledge that can't be digitized, "
            "complex interpersonal dynamics, moral/legal accountability, "
            "or real-world physical interaction.\n\n"
            "Advice: AI is merely an efficiency tool at the margins for you. "
            "Keep deepening your industry network, leadership, or hands-on expertise — "
            "these will become even scarcer and more valuable."
        ),
    },
    {
        "min": 6,
        "max": 7,
        "level": "minimal",
        "label_zh": "极低风险区",
        "label_en": "Minimal Risk Zone",
        "tag_zh": "高度安全区",
        "tag_en": "Highly Secure Zone",
        "advice_zh": (
            "您的工作几乎完全建立在不可替代的物理技能、生命安全责任或顶级专家权威之上。"
            "AI 在可预见的未来都无法触及您的核心价值。\n\n"
            "建议：继续精进您的专业技能，同时可以关注 AI 如何作为辅助工具提升您的工作效率。"
        ),
        "advice_en": (
            "Your work is almost entirely built on irreplaceable physical skills, "
            "life-safety responsibilities, or top-tier expert authority. "
            "AI cannot touch your core value for the foreseeable future.\n\n"
            "Advice: Keep honing your specialized skills, "
            "and explore how AI can serve as an auxiliary tool to boost your efficiency."
        ),
    },
]


def compute_result(answers: QuizAnswers) -> ScoreResult:
    job = JOBS_BY_ID.get(answers.job_id)
    if not job:
        raise ValueError(f"Unknown job ID: {answers.job_id}")

    # Check for override jobs (bypass normal scoring)
    override = OVERRIDE_JOBS.get(answers.job_id)
    if override:
        return ScoreResult(
            total_score=0,
            breakdown=[job["score"], 0, 0, 0, 0, 0],
            risk_level="override",
            risk_label_zh=override["label_zh"],
            risk_label_en=override["label_en"],
            advice_zh=override["result_zh"],
            advice_en=override["result_en"],
            job_name_zh=job["name_zh"],
            job_name_en=job["name_en"],
        )

    q1_score = job["score"]

    question_answers = [answers.q2, answers.q3, answers.q4, answers.q5, answers.q6]
    q_scores = [OPTION_SCORES[a] for a in question_answers]

    breakdown = [q1_score] + q_scores
    total = sum(breakdown)

    risk = next(r for r in RISK_LEVELS if r["min"] <= total <= r["max"])

    return ScoreResult(
        total_score=total,
        breakdown=breakdown,
        risk_level=risk["level"],
        risk_label_zh=f'{risk["label_zh"]} — {risk["tag_zh"]}',
        risk_label_en=f'{risk["label_en"]} — {risk["tag_en"]}',
        advice_zh=risk["advice_zh"],
        advice_en=risk["advice_en"],
        job_name_zh=job["name_zh"],
        job_name_en=job["name_en"],
    )
