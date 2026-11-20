import regex as re

from .khmer_number_parse import (
  DELIMITER_WORDS,
  MINUS_WORD,
  _KHMER_CHAR,
  _NUMBER_PART,
  _SEP,
  parse_span,
)

_NUM = rf"{_NUMBER_PART}(?:{_SEP}(?:{'|'.join(DELIMITER_WORDS)}){_SEP}{_NUMBER_PART})?"

USD_PATTERN = re.compile(
  rf"(?<!{_KHMER_CHAR})"
  rf"(?P<minus>{re.escape(MINUS_WORD)}{_SEP})?"
  rf"(?P<amount>{_NUM}){_SEP}ដុល្លារ"
  rf"(?:{_SEP}(?P<cents>{_NUMBER_PART}){_SEP}សេន)?"
  rf"(?!{_KHMER_CHAR})"
)

KHR_PATTERN = re.compile(
  rf"(?<!{_KHMER_CHAR})"
  rf"(?P<minus>{re.escape(MINUS_WORD)}{_SEP})?"
  rf"(?P<amount>{_NUM}){_SEP}រៀល"
  rf"(?!{_KHMER_CHAR})"
)


def _usd_replacer(match) -> str:
  amount = parse_span(match.group("amount"))
  cents = match.group("cents")
  if cents and "." not in amount:
    amount = f"{amount}.{int(parse_span(cents)):02d}"
  sign = "-" if match.group("minus") else ""
  return f"{sign}${amount}"


def _khr_replacer(match) -> str:
  amount = parse_span(match.group("amount"))
  sign = "-" if match.group("minus") else ""
  return f"{sign}{amount}៛"


def processor(text: str) -> str:
  """Convert spoken currency back to symbols.

  "មួយរយដុល្លារ▁ម្ភៃប្រាំសេន" -> "$100.25", "មួយរយ▁រៀល" -> "100៛"
  """
  text = USD_PATTERN.sub(_usd_replacer, text)
  text = KHR_PATTERN.sub(_khr_replacer, text)
  return text


__all__ = ["processor"]
