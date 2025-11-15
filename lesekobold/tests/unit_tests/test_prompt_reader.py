import pytest
from src.prompt_reader import load_prompt


@pytest.mark.unit_test
def test_load_prompt():
    rval = load_prompt("story_prompt.md")
    assert rval is not None
    assert isinstance(rval, str)
    assert len(rval) > 0
