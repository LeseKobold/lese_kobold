"""Readability related utilities: calculation and mappings.

Moved out of `agent_manager.py` for separation of concerns.
"""

from __future__ import annotations

import logging
import re
from typing import List, Tuple
from src.config import app_config
from src.utils.singleton import Singleton

import pydantic
from src.config import app_config

LONG_WORD_LENGTH = 6


class ReadabilityUtils(metaclass=Singleton):
    """Helper class for readability-related utilities that need cached resources.

    `basic_vocab` maps grade -> alphabetically sorted list of unique words.
    Implemented as a singleton to avoid reloading vocab files on every instantiation.
    """

    _basic_vocab: dict[int, list[str]] | None = None

    @property
    def basic_vocab(self) -> dict[int, list[str]]:
        if self._basic_vocab is None:
            self._init_basic_vocab()
        return self._basic_vocab

    def _init_basic_vocab(self) -> dict[int, list[str]]:
        """Load basic vocabulary files from `resources/basic_vocab` and return a dictionary of a set of words.
        Keys are grade levels (int), values are sets of words (str).

        The function looks for the `basic_vocab` directory under the project resources
        folder (using `get_resources_path()`) unless `vocab_dir` is provided.

        """

        # collect into temporary sets (ensure uniqueness), then convert to sorted lists
        vocab: dict[int, set[str]] = dict()

        # load all vocab files
        for path in app_config.BASIC_VOCAB_PATH.glob("**/*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
                # require explicit 'grade' token in filename (e.g. basic_vocabulary_grade_1_2)
                m = re.search(
                    r"grade[_-]?(\d+(?:[_-]\d+)*)", path.stem, flags=re.IGNORECASE
                )
                if not m:
                    # skip files that don't explicitly declare grades in their filename
                    logging.debug(
                        f"Skipping vocab file without 'grade' in name: {path.name}"
                    )
                    continue
                nums = re.split(r"[_-]+", m.group(1))
                grades = [int(g) for g in nums if g.isdigit()]
                words = text.splitlines()
            except Exception:
                continue

            for w in words:
                token = w.strip()
                if not token:
                    continue
                for g in grades:
                    vocab.setdefault(g, set()).add(token)

        # convert sets to alphabetically sorted lists for stable ordering
        self._basic_vocab = {
            g: sorted(list(words_set)) for g, words_set in vocab.items()
        }

    def get_basic_vocab_coverage(
        self, text: str, grade: int, case_sensitive: bool = False
    ) -> float:
        """Compute percentage of words in text that appear in the basic vocab for the given grade.

        Args:
            text: input text to check
            grade: grade level (1-13)
            case_sensitive: if True, match words case-sensitively; if False (default), normalize to lowercase

        Returns:
            percentage (0-100) of words found in the grade's vocabulary
        """
        words = re.findall(r"\b\w+\b", text)
        vocab_words = set(self.basic_vocab.get(grade, []))
        if not words:
            return 0.0

        if case_sensitive:
            matched = sum(1 for w in words if w in vocab_words)
        else:
            vocab_lower = {v.lower() for v in vocab_words}
            matched = sum(1 for w in words if w.lower() in vocab_lower)

        percentage = float(round((matched / len(words)) * 100.0, 2))
        return percentage


@staticmethod
def calculate_lix_score(text: str, long_word_length: int = LONG_WORD_LENGTH) -> float:
    """Calculate the LIX readability score for a given text.

    LIX = (words / sentences) + (long_words * 100 / words)
    where long_words are words with length greater than `long_word_length`.
    """
    if not text or not text.strip():
        return 0.0

    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"\b\w+\b", text)

    word_count = len(words)
    sentence_count = len(sentences) if len(sentences) > 0 else 1
    long_words = sum(1 for w in words if len(w) > int(long_word_length))

    logging.debug(
        f"LIX calculation details: word_count={word_count}, sentences={sentence_count}, long_words={long_words}"
    )

    if word_count == 0:
        return 0.0

    lix = (word_count / sentence_count) + (long_words * 100.0 / word_count)
    return float(round(lix, 2))


@staticmethod
def convert_lix_to_school_grade(lix: float) -> int:
    """Convert a LIX score to an approximate school grade level (1..13).

    13 corresponds to college (LIX 56+).
    """
    try:
        score = int(lix)
    except Exception:
        raise TypeError("lix must be a number")

    if score >= 56:
        return 13
    if 52 <= score <= 55:
        return 12
    if 48 <= score <= 51:
        return 11
    if 44 <= score <= 47:
        return 10
    if 40 <= score <= 43:
        return 9
    if 36 <= score <= 39:
        return 8
    if 32 <= score <= 35:
        return 7
    if 28 <= score <= 31:
        return 6
    if 24 <= score <= 27:
        return 5
    if 20 <= score <= 23:
        return 4
    if 15 <= score <= 19:
        return 3
    if 10 <= score <= 14:
        return 2
    return 1


@staticmethod
def convert_lix_to_frontread_school_grades(lix: float) -> List[int]:
    """Map a LIX score to one or more grade levels using the Frontread mapping.

    Returns list of integers (grades) that match the LIX ranges.
    """
    try:
        score = int(lix)
    except Exception:
        raise TypeError("lix must be a number")

    grade_ranges: dict[int, Tuple[float, float]] = {
        1: (0, 10),
        2: (0, 10),
        3: (10, 12),
        4: (15, 17),
        5: (15, 20),
        6: (20, 25),
        7: (25, 27),
        8: (20, 30),
        9: (30, 32),
        10: (32, 35),
    }

    matches: List[int] = []
    for grade, (low, high) in grade_ranges.items():
        if low <= score <= high:
            matches.append(grade)
    return matches


@staticmethod
def lix_to_worksheetcrafter_school_grades(lix: float) -> int:
    """Map a LIX score to elementary classes (WorksheetCrafter mapping).

    Returns:
      - 1..4 for matching classes
      - -1 if LIX < 19
      - 99 if LIX > 35
    """
    try:
        score = float(lix)
    except Exception:
        raise TypeError("lix must be a number")

    if score < 19:
        return -1
    if score < 24:
        return 1
    if score < 27:
        return 2
    if score < 30:
        return 3
    if score <= 35:
        return 4
    return 99


# calculate and return the grade a given text using the defined functions above calculate_lix_score and lix_to_worksheetcrafter_school_grades
@staticmethod
def get_grade_level(text: str) -> int | None:
    """Calculate the grade level for the given text and map it to WorksheetCrafter grades.

    Returns:
      - 1..4 for matching classes
      - -1 if LIX < 19
      - 99 if LIX > 35
      - None if the text is empty or None
    """
    # try catch exceptions and log them
    try:
        lix_score = calculate_lix_score(text)
        grade = lix_to_worksheetcrafter_school_grades(lix_score)
    except Exception as e:
        logging.error(f"Error calculating grade for text: {e}")
        return None
    return grade


@staticmethod
def get_basic_vocab_coverage(
    text: str, grade: int, case_sensitive: bool = False
) -> float:
    """Compute percentage of words in text that appear in the basic vocab for the given grade.

    Args:
        text: input text to check
        grade: grade level (1-13)
        case_sensitive: if True, match words case-sensitively; if False (default), normalize to lowercase

    Returns:
        percentage (0-100) of words found in the grade's vocabulary
    """
    return ReadabilityUtils().get_basic_vocab_coverage(text, grade, case_sensitive)
