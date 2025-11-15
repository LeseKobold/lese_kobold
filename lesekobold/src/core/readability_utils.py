"""LIX related utilities: calculation and mappings.

Moved out of `agent_manager.py` for separation of concerns.
"""

from __future__ import annotations

import logging
import re
from typing import List, Tuple

LONG_WORD_LENGTH = 6


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
