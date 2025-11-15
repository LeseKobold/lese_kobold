import pytest
import logging
from lesekobold.src.readability_utils import ReadabilityUtils


@pytest.mark.unit_test
def test_init_basic_vocab():
    ru = ReadabilityUtils()
    vocab = ru.basic_vocab

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
    coverage_case_sensitive = ru.get_basic_vocab_coverage(text, grade=1, case_sensitive=True)
    logging.debug(f"Coverage for grade 1: {coverage}")

    assert isinstance(coverage, float)
    assert coverage == 80.0  # 5 out of 10 words are in grade 1 vocab
    assert coverage_case_sensitive == 70