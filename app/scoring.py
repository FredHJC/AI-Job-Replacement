from app.data.jobs import JOBS_BY_ID, OVERRIDE_JOBS
from app.data.questions import QUESTIONS
from app.models import QuizAnswers, ScoreResult

OPTION_SCORES = {"A": 4, "B": 3, "C": 2, "D": 1}

# Raw score range: 6 (min: 1+5*1) to 27 (max: 7+5*4)
RAW_MIN = 6
RAW_MAX = 27


def raw_to_100(raw: int) -> int:
    """Map raw score (6-27) to 0-100 scale, integer, where higher = more risk."""
    return round((raw - RAW_MIN) / (RAW_MAX - RAW_MIN) * 100)


# 5-level risk system based on 100-point scale
RISK_LEVELS = [
    {
        "min": 86, "max": 100,   # raw 24-27
        "level": "extreme",
        "label_zh": "极高风险",
        "label_en": "Extreme Risk",
        "tag_zh": "自动化重灾区",
        "tag_en": "Automation Ground Zero",
        "advice_zh": (
            "您的工作高度集中在重复性信息处理和标准化执行层面。"
            "当前 AI 的能力已经可以直接覆盖您的大部分核心任务。\n\n"
            '建议：迫切需要向"复杂决策"、"人际协调"或"AI 审查者"的方向转型。'
        ),
        "advice_en": (
            "Your work is heavily concentrated in repetitive information processing "
            "and standardized execution. Current AI can already cover most of your core tasks.\n\n"
            "Advice: Urgently pivot toward complex decision-making, "
            "interpersonal coordination, or AI oversight roles."
        ),
    },
    {
        "min": 67, "max": 85,   # raw 20-23
        "level": "high",
        "label_zh": "高风险",
        "label_en": "High Risk",
        "tag_zh": "AI 深度冲击区",
        "tag_en": "AI Deep Impact Zone",
        "advice_zh": (
            "您的工作虽然需要专业技能，但核心产出的结构化程度较高，"
            "AI 已经能在很大程度上辅助甚至替代部分环节。\n\n"
            "建议：深度掌握 AI 工具，将自己定位为 AI 产出的审核者和把关者，"
            "而非与 AI 竞争同一类任务。"
        ),
        "advice_en": (
            "While your work requires professional skills, the core output is fairly structured — "
            "AI can already assist or replace significant parts of it.\n\n"
            "Advice: Master AI tools deeply. Position yourself as the reviewer and quality gate "
            "for AI output, rather than competing on the same tasks."
        ),
    },
    {
        "min": 38, "max": 66,   # raw 14-19
        "level": "moderate",
        "label_zh": "中等风险",
        "label_en": "Moderate Risk",
        "tag_zh": "人机协作区",
        "tag_en": "Human-AI Collaboration Zone",
        "advice_zh": (
            '您的工作处于 AI 能力的"锯齿状前沿"上 — 有些环节 AI 很擅长，'
            "有些则完全无法触及。您的竞争优势在于经验判断和跨领域整合能力。\n\n"
            "建议：主动将 AI 融入工作流程以提升效率，同时持续加深行业理解和人际网络。"
        ),
        "advice_en": (
            "Your work sits on AI's 'jagged frontier' — AI excels at some parts "
            "but can't touch others. Your edge is experience-based judgment and cross-domain integration.\n\n"
            "Advice: Proactively integrate AI into your workflow for efficiency gains, "
            "while deepening your industry expertise and professional network."
        ),
    },
    {
        "min": 15, "max": 37,   # raw 9-13
        "level": "low",
        "label_zh": "较低风险",
        "label_en": "Low Risk",
        "tag_zh": "护城河稳固区",
        "tag_en": "Strong Moat Zone",
        "advice_zh": (
            '您的工作高度依赖无法被数字化的"隐性知识"、复杂的人际博弈、'
            "道德法律责任，或面对面的真实交互。\n\n"
            "建议：AI 对您来说主要是一个边际效率工具。"
            "继续深耕您的行业人脉、领导力和专业技能，这些在未来会更加稀缺。"
        ),
        "advice_en": (
            "Your work heavily depends on tacit knowledge, complex interpersonal dynamics, "
            "moral/legal accountability, or real-world face-to-face interaction.\n\n"
            "Advice: AI is mainly a marginal efficiency tool for you. "
            "Keep deepening your network, leadership, and specialized skills — "
            "they'll become even scarcer and more valuable."
        ),
    },
    {
        "min": 0, "max": 14,   # raw 6-8
        "level": "minimal",
        "label_zh": "极低风险",
        "label_en": "Minimal Risk",
        "tag_zh": "高度安全区",
        "tag_en": "Highly Secure Zone",
        "advice_zh": (
            "您的工作建立在不可替代的物理技能、生命安全责任或权威决策权之上。"
            "AI 在可预见的未来无法触及您的核心价值。\n\n"
            "建议：继续精进专业技能，关注 AI 作为辅助工具如何提升您的工作效率。"
        ),
        "advice_en": (
            "Your work is built on irreplaceable physical skills, "
            "life-safety responsibilities, or authoritative decision-making. "
            "AI cannot touch your core value for the foreseeable future.\n\n"
            "Advice: Keep honing your expertise, and explore how AI can "
            "serve as an auxiliary tool to boost your efficiency."
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
    raw_total = sum(breakdown)
    score_100 = raw_to_100(raw_total)

    risk = next(r for r in RISK_LEVELS if r["min"] <= score_100 <= r["max"])

    return ScoreResult(
        total_score=score_100,
        breakdown=breakdown,
        risk_level=risk["level"],
        risk_label_zh=f'{risk["label_zh"]} — {risk["tag_zh"]}',
        risk_label_en=f'{risk["label_en"]} — {risk["tag_en"]}',
        advice_zh=risk["advice_zh"],
        advice_en=risk["advice_en"],
        job_name_zh=job["name_zh"],
        job_name_en=job["name_en"],
    )
