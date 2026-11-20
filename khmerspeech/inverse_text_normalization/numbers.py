from .khmer_number_parse import NUMBER_SPAN_RE, parse_span


def processor(text: str) -> str:
  """Convert spoken Khmer numbers (cardinals and decimals) back to digits.

  "មួយរយ▁ម្ភៃបី" -> "123", "ដក▁មួយរយ▁ម្ភៃបី▁ចុច▁សែសិបប្រាំ" -> "-123.45"
  """
  return NUMBER_SPAN_RE.sub(lambda m: parse_span(m.group(0)), text)


__all__ = ["processor"]
