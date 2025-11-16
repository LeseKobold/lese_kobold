import pytest
from src.core.prompt_reader import load_prompt
from src.core.readability_utils import get_grade_level


@pytest.mark.unit_test
def test_load_prompt():
    rval = load_prompt("story_prompt.md")
    assert rval is not None
    assert isinstance(rval, str)
    assert len(rval) > 0


@pytest.mark.unit_test
def test_load_prompt_with_variables():
    rval = load_prompt(
        "style_prompt.md",
        variables={"get_grade_level": get_grade_level.__name__},
    )
    assert rval is not None
    assert isinstance(rval, str)
