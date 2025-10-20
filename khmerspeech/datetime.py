# -*- coding: utf-8 -*-
import regex as re
from khmerspeech.strings import overwrite_spans


"""
  Matches times like 12:30, 7:05pm, ០៨:៥៩ AM.
  Hours = 1–2 digits; minutes = exactly 2 digits.
  Digits can be Arabic 0-9 or Khmer \u17e0–\u17e9.
  Optional am|pm|AM|PM (with an optional space before it).
"""
RE_ONLY_TIME = re.compile(
  r"([0-9\u17e0-\u17e9]{1,2}):([0-9\u17e0-\u17e9]{2})\s?(am|pm|AM|PM)?"
)

"""
Matches YYYY-MM-DD or YYYY/MM/DD, with Arabic or Khmer digits.
Uses a backreference \2 so the same separator (- or /) must be used between year–month and month–day.
Examples: 2025-10-20, ២០២៥/១០/២០.
"""
RE_DATE_YEAR_FIRST = re.compile(
  r"([\u17e0-\u17e9\d]{4})([/-])([\u17e0-\u17e9\d]{2})\2([\u17e0-\u17e9\d]{2})"
)


"""
Matches DD-MM-YYYY or DD/MM/YYYY, again with Arabic or Khmer digits and consistent separator.
Examples: 20/10/2025, ២០-១០-២០២៥.
"""
RE_DATE_DAY_FIRST = re.compile(
  r"([\u17e0-\u17e9\d]{2})([/-])([\u17e0-\u17e9\d]{2})\2([\u17e0-\u17e9\d]{4})"
)


def date_processor(text: str) -> str:
  replacements = []

  for m in RE_DATE_YEAR_FIRST.finditer(text):
    replacement = f"{m[1]} {m[3]} {m[4]}"
    replacements.append((m.start(), m.end(), replacement))

  for m in RE_DATE_DAY_FIRST.finditer(text):
    replacement = f"{m[1]} {m[3]} {m[4]}"
    replacements.append((m.start(), m.end(), replacement))

  return overwrite_spans(text, replacements)


def time_processor(text: str) -> str:
  replacements = []
  for m in RE_ONLY_TIME.finditer(text):
    replacement = f"{m[1]} {m[2]}"
    if m[3] is not None:
      replacement += "▁" + "▁".join(m[3])
    replacements.append((m.start(), m.end(), replacement))
  return overwrite_spans(text, replacements)
