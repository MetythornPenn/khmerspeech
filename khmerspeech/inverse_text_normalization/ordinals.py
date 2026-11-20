import regex as re

from .khmer_number_parse import _KHMER_CHAR, _NUMBER_PART, _SEP, parse_span

ORDINAL_PATTERN = re.compile(
  rf"(?<!{_KHMER_CHAR})ទី{_SEP}(?P<number>{_NUMBER_PART})(?!{_KHMER_CHAR})"
)


def processor(text: str) -> str:
  """Convert spoken Khmer ordinals back to digits: "ទី▁ប្រាំ" -> "ទី5"."""
  return ORDINAL_PATTERN.sub(lambda m: f"ទី{parse_span(m.group('number'))}", text)


__all__ = ["processor"]
