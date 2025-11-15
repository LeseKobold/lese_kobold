import pytest

from lesekobold.src.config import app_config
from lesekobold.src.core.readability_utils import (
    calculate_lix_score,
    convert_lix_to_frontread_school_grades,
    convert_lix_to_school_grade,
    lix_to_worksheetcrafter_school_grades,
)



@pytest.mark.unit_test
def test_calculate_lix_score_for_text():
    # 30 words, 2 sentences, 7 long words (>6 chars) -> LIX = (32/2) + (7*100/32) = 16 + 21.875 = 37.875 -> 38.33
    text = "In einem kleinen Dorf, zwischen alten Eichen und duftenden Apfelbäumen, lebte ein Kobold namens Klemens. Er war nicht groß — kaum größer als ein Laubhaufen — und trug stets eine bunte Zipfelmütze."
    score = calculate_lix_score(text)
    assert isinstance(score, float)
    assert score == 38.33


@pytest.mark.unit_test
def test_calculate_lix_score_from_resource():
    resource = app_config.STORIES_PATH / "der-vorlesende-kobold.txt"
    assert resource.exists(), f"Resource not found at {resource}"

    text = resource.read_text(encoding="utf-8")

    # the sample text contains 288 words, 18 sentences, and 78 long words (>6 chars)
    score = calculate_lix_score(text)
    assert isinstance(score, float)
    assert score == 43.08


@pytest.mark.unit_test
def test_convert_lix_to_school_grade():
    lix = 43.08
    grade = convert_lix_to_school_grade(lix)
    assert isinstance(grade, int)
    assert grade == 9


@pytest.mark.unit_test
def test_convert_lix_to_frontread_school_grades():
    lix = 24
    grades = convert_lix_to_frontread_school_grades(lix)
    assert isinstance(grades, list)
    assert all(isinstance(g, int) for g in grades)
    assert grades == [6, 8]


@pytest.mark.unit_test
def test_lix_to_worksheetcrafter_school_grades():
    lix = 28
    grade = lix_to_worksheetcrafter_school_grades(lix)
    assert isinstance(grade, int)
    assert grade == 3
