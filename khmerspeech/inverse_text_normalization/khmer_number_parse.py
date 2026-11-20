"""Core parser that converts spoken Khmer number words back into digits.

This is the inverse of ``text_normalization.khmer_number_verbalize``. The
verbalizer concatenates the words of one scale group (``សាមសិបបួន``,
``ម្ភៃបីលាន``) and joins groups with ``▁`` or a space, so the separator is
meaningful: chunks are parsed with greedy longest-word matching, then
combined into numbers while their scales descend.
"""

import regex as re

DIGITS = {
  "សូន្យ": 0,
  "មួយ": 1,
  "ពីរ": 2,
  "បី": 3,
  "បួន": 4,
  "ប្រាំ": 5,
  "ប្រាំមួយ": 6,
  "ប្រាំពីរ": 7,
  "ប្រាំបី": 8,
  "ប្រាំបួន": 9,
}

TENS = {
  "ដប់": 10,
  "ម្ភៃ": 20,
  "សាមសិប": 30,
  "សែសិប": 40,
  "ហាសិប": 50,
  "ហុកសិប": 60,
  "ចិតសិប": 70,
  "ប៉ែតសិប": 80,
  "កៅសិប": 90,
}

HUNDRED = {"រយ": 100}

SCALES = {
  "ពាន់": 10**3,
  "ម៉ឺន": 10**4,
  "សែន": 10**5,
  "លាន": 10**6,
  "ប៊ីលាន": 10**9,
  "ទ្រីលាន": 10**12,
  "ក្វាទ្រីលាន": 10**15,
  "គ្វីនទីលាន": 10**18,
  "សិចទីលាន": 10**21,
  "សិបទីលាន": 10**24,
  "អុកទីលាន": 10**27,
  "ណូនីលាន": 10**30,
  "ដេស៊ីលាន": 10**33,
  "អាន់ដេស៊ីលាន": 10**36,
}

MINUS_WORD = "ដក"
DELIMITER_WORDS = {"ចុច": ".", "ក្បៀស": ","}

_NUMBER_WORDS = {**DIGITS, **TENS, **HUNDRED, **SCALES}


def _alternation(words) -> str:
  # Longest-first so ប្រាំមួយ wins over ប្រាំ, សិបទីលាន over similar prefixes.
  return "(?:" + "|".join(map(re.escape, sorted(words, key=len, reverse=True))) + ")"


TOKEN_RE = re.compile(_alternation(_NUMBER_WORDS))

_NUM_WORD = _alternation(_NUMBER_WORDS)
# The verbalizer never emits a bare multiplier (រយ/លាន/...) — every number
# starts with a digit or tens word, which keeps prose like "រាប់លាន" intact.
_LEAD_WORD = _alternation({**DIGITS, **TENS})
_SEP = "[▁ ]*"
_KHMER_CHAR = "[ក-៝]"
_NUMBER_PART = rf"{_LEAD_WORD}(?:{_SEP}{_NUM_WORD})*"
_DELIMITER_RE = re.compile("|".join(DELIMITER_WORDS))
_CHUNK_SPLIT_RE = re.compile(r"[▁ ]+")

# A spoken number span: optional minus, integer words, optional decimal part.
# Guarded so it never starts or ends inside a longer Khmer word (e.g. រយៈពេល).
NUMBER_SPAN_RE = re.compile(
  rf"(?<!{_KHMER_CHAR})"
  rf"(?:{re.escape(MINUS_WORD)}{_SEP})?"
  rf"{_NUMBER_PART}"
  rf"(?:{_SEP}(?:ចុច|ក្បៀស){_SEP}{_NUMBER_PART})?"
  rf"(?!{_KHMER_CHAR})"
)


def words_to_int(words) -> int:
  """Value of one concatenated group, e.g. [មួយ, រយ, ម្ភៃ, បី] -> 123."""
  total = 0
  current = 0
  for word in words:
    if word in DIGITS:
      current += DIGITS[word]
    elif word in TENS:
      current += TENS[word]
    elif word in HUNDRED:
      current = max(current, 1) * 100
    else:
      total += max(current, 1) * SCALES[word]
      current = 0
  return total + current


def _chunk_rank(words) -> int:
  """Scale rank of a chunk, taken from its trailing scale word."""
  last = words[-1]
  if last in SCALES:
    return SCALES[last]
  if last in HUNDRED:
    return 100
  return 1


def combine_chunks(chunks) -> list:
  """Combine per-chunk values into numbers while their scales descend.

  ["មួយរយ", "ម្ភៃបី"] is one number (123) because 100 -> 1 descends, while
  ["ដប់", "មួយរយ"] is two numbers (10, 100) because the scale rises. A rise
  into a big scale instead closes a multiplier: ["មួយរយ", "ម្ភៃបីលាន"] is
  (100 + 23) * 10^6.
  """
  numbers = []
  total = 0
  current = 0
  prev_rank = None

  for words in chunks:
    value = words_to_int(words)
    rank = _chunk_rank(words)

    if prev_rank is not None and rank >= prev_rank:
      if rank > prev_rank and rank >= 1000:
        # Ascending into a big scale: pending chunks are its multiplier.
        total += current * rank + value
        current = 0
        prev_rank = rank
        continue
      # Equal or ascending into a small scale: a new number starts.
      numbers.append(total + current)
      total = 0
      current = 0

    if rank >= 1000:
      total += value
    else:
      current += value
    prev_rank = rank

  numbers.append(total + current)
  return numbers


def _to_chunks(part: str):
  chunks = []
  for chunk in _CHUNK_SPLIT_RE.split(part):
    words = TOKEN_RE.findall(chunk)
    if words:
      chunks.append(words)
  return chunks


def parse_span(span: str) -> str:
  """Convert one matched spoken-number span into its written form.

  Multiple adjacent numbers are joined with single spaces; a decimal
  delimiter applies to the last number before it.
  """
  span = span.strip("▁ ")
  sign = ""
  if span.startswith(MINUS_WORD):
    sign = "-"
    span = span[len(MINUS_WORD) :].strip("▁ ")

  delimiter_match = _DELIMITER_RE.search(span)
  if delimiter_match:
    delimiter = DELIMITER_WORDS[delimiter_match.group(0)]
    integer_part = span[: delimiter_match.start()]
    fraction_part = span[delimiter_match.end() :]
  else:
    delimiter = ""
    integer_part = span
    fraction_part = ""

  values = [str(v) for v in combine_chunks(_to_chunks(integer_part))] or ["0"]

  if delimiter and fraction_part:
    # Leading zeros and digit-by-digit fractions come out as separate
    # values, so joining them reconstructs the digit string exactly:
    # [0, 0, 12] -> "0012", [1, 2, 3, 4] -> "1234", [45] -> "45".
    fraction = "".join(str(v) for v in combine_chunks(_to_chunks(fraction_part)))
    values[-1] = f"{values[-1]}{delimiter}{fraction}"

  return sign + " ".join(values)


__all__ = [
  "DIGITS",
  "TENS",
  "HUNDRED",
  "SCALES",
  "MINUS_WORD",
  "DELIMITER_WORDS",
  "NUMBER_SPAN_RE",
  "combine_chunks",
  "words_to_int",
  "parse_span",
]
