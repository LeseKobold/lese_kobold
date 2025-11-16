import pytest
import logging

from src.config import app_config
from src.core.readability_utils import (
    calculate_lix_score,
    convert_lix_to_frontread_school_grades,
    convert_lix_to_school_grade,
    lix_to_worksheetcrafter_school_grades,
    get_grade_level,
    ReadabilityUtils,
)


@pytest.fixture
def readability_utils() -> ReadabilityUtils:
    return ReadabilityUtils()


@pytest.fixture
def sample_text_grade_4() -> str:
    return (
        "Der Kindergarten geht heute Abend Laternen laufen. "
        "Dafür treffen sich die Kinder um sechs Uhr am Spielplatz. "
        "Alle Kinder haben bunte Laternen."
    )


@pytest.fixture
def sample_text_grade_1() -> str:
    # LIX 19.32 -> grade 1
    return (
        "Wir backen heute Kuchen. "
        "Wir fangen damit an, den Teig zu rühren. "
        "Danach geben wir Backpulver dazu. "
        "Dann kommt der Kuchen in eine Kuchenform. "
        "Dann kommt der Kuchen auf das Backblech. Dann stellen wir das Backblech in den Ofen."
    )


@pytest.mark.unit_test
def test_init_basic_vocab():
    vocab = readability_utils.basic_vocab

    assert isinstance(vocab, dict)
    assert all(isinstance(k, int) for k in vocab.keys())
    assert all(isinstance(v, list) for v in vocab.values())
    assert all(all(isinstance(word, str) for word in words) for words in vocab.values())

    assert "packst" in vocab.get(1, [])
    assert "ärgerst" not in vocab.get(1, [])


@pytest.mark.unit_test
def test_get_basic_vocab_coverage():
    ru = ReadabilityUtils()
    text = "Die Brüder ärgern sich über die Katze, die immer faucht."
    coverage = ru.get_basic_vocab_coverage(text, grade=1)
    coverage_case_sensitive = ru.get_basic_vocab_coverage(
        text, grade=1, case_sensitive=True
    )
    logging.debug(f"Coverage for grade 1: {coverage}")

    assert isinstance(coverage, float)
    assert coverage == 80.0  # 5 out of 10 words are in grade 1 vocab
    assert coverage_case_sensitive == 70


@pytest.mark.unit_test
def test_calculate_lix_score_for_text():
    # 30 words, 2 sentences, 7 long words (>6 chars) -> LIX = (32/2) + (7*100/32) = 16 + 21.875 = 37.875 -> 38.33
    text = "Der Kindergarten geht heute Abend Laternen laufen. Dafür treffen sich die Kinder um sechs Uhr am Spielplatz. Alle Kinder haben bunte Laternen."
    score = calculate_lix_score(text)
    assert isinstance(score, float)
    assert score == 30.06


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


@pytest.mark.unit_test
def test_get_grade_level(sample_text_grade_4, sample_text_grade_1):
    assert get_grade_level(sample_text_grade_4) == 4
    assert get_grade_level(sample_text_grade_1) == 1
