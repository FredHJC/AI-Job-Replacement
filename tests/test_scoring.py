import pytest
from app.models import QuizAnswers
from app.scoring import compute_result


def make_answers(job_id="programmer", q2="A", q3="A", q4="A", q5="A", q6="A"):
    return QuizAnswers(job_id=job_id, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6)


def test_max_score():
    result = compute_result(make_answers())
    assert result.total_score == 24
    assert result.risk_level == "extreme"
    assert result.breakdown == [4, 4, 4, 4, 4, 4]


def test_min_score():
    result = compute_result(make_answers(job_id="surgeon", q2="D", q3="D", q4="D", q5="D", q6="D"))
    assert result.total_score == 6
    assert result.risk_level == "minimal"
    assert result.breakdown == [1, 1, 1, 1, 1, 1]


def test_mid_score():
    result = compute_result(make_answers(job_id="backend_dev", q2="B", q3="B", q4="B", q5="B", q6="B"))
    assert result.total_score == 18
    assert result.risk_level == "high"


def test_low_risk_range():
    result = compute_result(make_answers(job_id="k12_teacher", q2="C", q3="C", q4="C", q5="C", q6="C"))
    assert result.total_score == 12
    assert result.risk_level == "low"


def test_bilingual_output():
    result = compute_result(make_answers())
    assert "极高风险区" in result.risk_label_zh
    assert "Extreme Risk Zone" in result.risk_label_en
    assert result.job_name_zh == "程序员"
    assert result.job_name_en == "Programmer"


def test_unknown_job_raises():
    with pytest.raises(ValueError, match="Unknown job ID"):
        compute_result(make_answers(job_id="nonexistent_job"))


def test_all_risk_boundaries():
    # 24 = extreme
    result = compute_result(make_answers(job_id="programmer", q2="A", q3="A", q4="A", q5="A", q6="A"))
    assert result.risk_level == "extreme"

    # 16 = high (3+3+2+3+2+3)
    result = compute_result(make_answers(job_id="backend_dev", q2="B", q3="C", q4="B", q5="C", q6="B"))
    assert result.total_score == 16
    assert result.risk_level == "high"

    # 7 = minimal
    result = compute_result(make_answers(job_id="surgeon", q2="C", q3="D", q4="D", q5="D", q6="D"))
    assert result.total_score == 7
    assert result.risk_level == "minimal"


def test_government_jobs():
    result = compute_result(make_answers(job_id="civil_servant", q2="B", q3="B", q4="B", q5="B", q6="B"))
    assert result.total_score == 18
    assert result.job_name_zh == "公务员(科员)"


def test_finance_expanded():
    result = compute_result(make_answers(job_id="ib_analyst", q2="A", q3="A", q4="A", q5="A", q6="A"))
    assert result.total_score == 23
    assert result.job_name_en == "Investment Banking Analyst"


def test_override_military():
    result = compute_result(make_answers(job_id="military"))
    assert result.risk_level == "override"
    assert result.total_score == 0
    assert "军人" in result.job_name_zh


def test_override_judge():
    result = compute_result(make_answers(job_id="judge"))
    assert result.risk_level == "override"
    assert "司法" in result.advice_zh


def test_override_firefighter():
    result = compute_result(make_answers(job_id="firefighter"))
    assert result.risk_level == "override"
