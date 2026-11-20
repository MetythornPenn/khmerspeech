"""Inverse text normalization: spoken/verbalized Khmer back to written form.

This package reverses ``khmerspeech.text_normalization`` so ASR output (or
TTS training text) can be rendered in written form again:

  "មួយរយដុល្លារ▁ម្ភៃប្រាំសេន" -> "$100.25"
  "ដក▁មួយរយ▁ម្ភៃបី▁ចុច▁សែសិបប្រាំ" -> "-123.45"
"""

import regex as re

from . import currency, datetime, numbers, ordinals, phone_numbers, urls
from .khmer_number_parse import parse_span, words_to_int

_RE_SOFT_SEP = re.compile(r"▁")
_RE_SPACES = re.compile(r"\s+")


def inverse_normalize(text: str) -> str:
  """Run the full inverse-normalization pipeline over the text.

  Order matters: currency and ordinals consume their surrounding keywords
  before the generic number pass, while phone numbers, times, and dates are
  reassembled from the digits the number pass produces.
  """
  text = currency.processor(text)
  text = ordinals.processor(text)
  text = numbers.processor(text)
  text = phone_numbers.processor(text)
  text = datetime.processor(text)
  text = urls.processor(text)
  # Remaining soft separators come from processors without a written inverse
  # (e.g. dictionary units); render them as plain spaces.
  text = _RE_SOFT_SEP.sub(" ", text)
  text = _RE_SPACES.sub(" ", text).strip()
  return text


__all__ = [
  "currency",
  "datetime",
  "numbers",
  "ordinals",
  "phone_numbers",
  "urls",
  "inverse_normalize",
  "parse_span",
  "words_to_int",
]
