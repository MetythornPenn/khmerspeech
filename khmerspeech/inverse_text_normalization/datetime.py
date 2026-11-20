import regex as re

# Output of text_normalization.datetime.time_processor: "10 23▁A▁M"
TIME_PATTERN = re.compile(
  r"\b(?P<hour>\d{1,2}) (?P<minute>\d{2})▁(?P<meridiem>[APap])▁[Mm]\b"
)

# Dates flattened by the forward pass ("2024-01-02" -> "2024 01 02"), after
# cardinal verbalization and the inverse number pass ("2024 1 2").
YEAR_FIRST_PATTERN = re.compile(
  r"(?<!\d)(?P<year>(?:19|20)\d{2}) (?P<month>\d{1,2}) (?P<day>\d{1,2})(?!\d)"
)
DAY_FIRST_PATTERN = re.compile(
  r"(?<!\d)(?P<day>\d{1,2}) (?P<month>\d{1,2}) (?P<year>(?:19|20)\d{2})(?!\d)"
)


def _time_replacer(match) -> str:
  meridiem = match.group("meridiem").upper()
  return f"{match.group('hour')}:{match.group('minute')}{meridiem}M"


def _date_replacer(match, year_first: bool) -> str:
  month = int(match.group("month"))
  day = int(match.group("day"))
  if not (1 <= month <= 12 and 1 <= day <= 31):
    return match.group(0)
  year = match.group("year")
  if year_first:
    return f"{year}-{month:02d}-{day:02d}"
  return f"{day:02d}-{month:02d}-{year}"


def processor(text: str) -> str:
  """Rebuild clock times and numeric dates.

  "10 23▁A▁M" -> "10:23AM", "2024 1 2" -> "2024-01-02"
  """
  text = TIME_PATTERN.sub(_time_replacer, text)
  text = YEAR_FIRST_PATTERN.sub(lambda m: _date_replacer(m, True), text)
  text = DAY_FIRST_PATTERN.sub(lambda m: _date_replacer(m, False), text)
  return text


__all__ = ["processor"]
