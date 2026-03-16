import pytest
from app.models import QuizAnswers
from app.scoring import compute_result, raw_to_100


def make_answers(job_id="programmer", q2="A", q3="A", q4="A", q5="A", q6="A"):
    return QuizAnswers(job_id=job_id, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6)


def test_raw_to_100():
    assert raw_to_100(6) == 0     # min raw
    assert raw_to_100(27) == 100  # max raw
    assert raw_to_100(17) == 52   # midpoint-ish


def test_max_score():
    # programmer(6) + 5*A(4) = 26 → raw_to_100(26) = 95
    result = compute_result(make_answers())
    assert result.total_score == 95
    assert result.risk_level == "extreme"


def test_absolute_max():
    # data_entry(7) + 5*A(4) = 27 → 100
    result = compute_result(make_answers(job_id="data_entry"))
    assert result.total_score == 100
    assert result.risk_level == "extreme"


def test_min_score():
    # surgeon(1) + 5*D(1) = 6 → 0
    result = compute_result(make_answers(job_id="surgeon", q2="D", q3="D", q4="D", q5="D", q6="D"))
    assert result.total_score == 0
    assert result.risk_level == "minimal"


def test_mid_score():
    # backend_dev(5) + 5*B(3) = 20 → raw_to_100(20) = 67
    result = compute_result(make_answers(job_id="backend_dev", q2="B", q3="B", q4="B", q5="B", q6="B"))
    assert result.total_score == 67
    assert result.risk_level == "high"


def test_low_risk():
    # k12_teacher(3) + 5*C(2) = 13 → raw_to_100(13) = 33
    result = compute_result(make_answers(job_id="k12_teacher", q2="C", q3="C", q4="C", q5="C", q6="C"))
    assert result.total_score == 33
    assert result.risk_level == "low"


def test_moderate_risk():
    # product_manager(3) + 5*B(3) = 18 → raw_to_100(18) = 57
    result = compute_result(make_answers(job_id="product_manager", q2="B", q3="B", q4="B", q5="B", q6="B"))
    assert result.total_score == 57
    assert result.risk_level == "moderate"


def test_bilingual_output():
    result = compute_result(make_answers())
    assert "极高风险" in result.risk_label_zh
    assert "Extreme Risk" in result.risk_label_en
    assert result.job_name_zh == "程序员"


def test_unknown_job_raises():
    with pytest.raises(ValueError, match="Unknown job ID"):
        compute_result(make_answers(job_id="nonexistent_job"))


def test_override_military():
    result = compute_result(make_answers(job_id="military"))
    assert result.risk_level == "override"
    assert result.total_score == 0


def test_override_judge():
    result = compute_result(make_answers(job_id="judge"))
    assert result.risk_level == "override"
    assert "司法" in result.advice_zh


def test_override_firefighter():
    result = compute_result(make_answers(job_id="firefighter"))
    assert result.risk_level == "override"
