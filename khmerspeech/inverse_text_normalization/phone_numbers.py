import regex as re

# Output of text_normalization.phone_numbers before cardinal verbalization:
# "0▁10▁123▁123"
CHUNKED_PATTERN = re.compile(r"(?<![\d▁])0▁\d{2}(?:▁\d{1,4})+(?![\d▁])")

# After the number pass, a fully verbalized phone number comes back as
# space-separated chunks: "0 10 123 123"
SPOKEN_PATTERN = re.compile(r"(?<!\d)0 \d{2}(?: \d{2,4}){2,3}(?!\d)")


def _join_if_phone_length(match) -> str:
  digits = match.group(0).replace(" ", "")
  if 9 <= len(digits) <= 11:
    return digits
  return match.group(0)


def processor(text: str) -> str:
  """Rejoin chunked phone numbers: "0▁10▁123▁123" -> "010123123"."""
  text = CHUNKED_PATTERN.sub(lambda m: m.group(0).replace("▁", ""), text)
  text = SPOKEN_PATTERN.sub(_join_if_phone_length, text)
  return text


__all__ = ["processor"]
