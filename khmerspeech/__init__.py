import regex as re

from . import inverse_text_normalization, text_normalization
from .inverse_text_normalization import inverse_normalize
from .text_normalization import (
  ascii_lines,
  cardinals,
  currency,
  datetime,
  decimals,
  dictionary,
  hashtags,
  license_plate,
  normalize,
  ordinals,
  parenthesis,
  phone_numbers,
  punctuations,
  quotings,
  repeater,
  urls,
)
from .text_normalization.dictionary import dict_verbalize

_RE_SPACES = re.compile(r"\s+")


def _verbalize(text: str) -> str:
  """Shared verbalization steps for both TTS and ASR normalization."""
  text = phone_numbers.processor(text, chunk_size=3)
  text = datetime.date_processor(text)
  text = datetime.time_processor(text)
  text = urls.processor(text)
  text = repeater.processor(text)
  text = currency.processor(text)
  text = cardinals.processor(text)
  text = decimals.processor(text)
  text = ordinals.processor(text)
  text = punctuations.processor(text)
  return text


def tts_normalize(text: str) -> str:
  """Normalize written text into a verbalized form for TTS training."""
  text = normalize.processor(text)
  text = dict_verbalize(text)
  text = _verbalize(text)
  text = text.replace("…", " ").replace("•", " ")
  return _RE_SPACES.sub(" ", text).strip()


def tts_gemini_normalize(text: str) -> str:
  """Normalize written text into a verbalized form for TTS training."""
  text = normalize.processor(text)
  text = dict_verbalize(text)
  text = _verbalize(text)
  text = text.replace("…", " ").replace("•", " ")
  return _RE_SPACES.sub(" ", text).strip()


def asr_normalize(text: str) -> str:
  """Normalize written text into a verbalized form for ASR training."""
  text = normalize.processor(text)
  text = _verbalize(text)
  text = dict_verbalize(text)
  return _RE_SPACES.sub(" ", text).strip()


# Backward-compatible alias for the pre-0.3 name.
TN = tts_normalize
ITN = inverse_normalize


__all__ = [
  "ascii_lines",
  "cardinals",
  "currency",
  "datetime",
  "decimals",
  "dictionary",
  "dict_verbalize",
  "hashtags",
  "inverse_normalize",
  "inverse_text_normalization",
  "license_plate",
  "normalize",
  "ordinals",
  "parenthesis",
  "phone_numbers",
  "punctuations",
  "quotings",
  "repeater",
  "text_normalization",
  "urls",
  "tts_normalize",
  "asr_normalize",
  "TN",
  "ITN",
]
