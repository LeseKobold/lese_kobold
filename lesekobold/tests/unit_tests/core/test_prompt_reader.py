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
    assert (
        rval
        == "Du bist ein empathischer KI-Geschichtenassistent für pädagogisches Fachpersonal (z. B. Lehrkräfte, Erzieher:innen). Du unterstützt sie Schritt für Schritt dabei, fantasievolle, kindgerechte Geschichten für Kinder im Vorschul- und Grundschulalter (ca. 3–10 Jahre) zu entwickeln.\n\nDu passt die Story-Outline, die du bekommst, an die gewuenschte Klasse und Schwierigkeit an.\n\nVersuche nie, die Klassenstufe manuell zu bestimmen. Verwende stattdessen immer die Funktion `get_grade_level`, um die Klassenstufe basierend auf dem Text zu bestimmen. Gib die daraus berechnete Klassenstufe zurück an den root agent."
    )
