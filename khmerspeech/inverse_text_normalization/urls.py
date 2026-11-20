import regex as re

# TLDs the forward URL verbalizer commonly produces; keeping this list tight
# avoids rewriting ordinary English sentences containing the word "dot".
KNOWN_TLDS = {
  "com", "org", "net", "edu", "gov", "info", "biz", "io", "co", "ai", "dev",
  "app", "me", "kh", "us", "sg", "ru", "th", "la", "vn", "cn", "jp", "kr",
  "uk", "fr", "de", "au", "in", "per",
}

_PART = r"[A-Za-z0-9▁-]+"

DOMAIN_PATTERN = re.compile(rf"\b{_PART}(?:\s+dot\s+{_PART})+\b")
EMAIL_PATTERN = re.compile(
  rf"\b(?P<user>[A-Za-z0-9▁._-]+)\s+at\s+(?P<domain>{_PART}(?:\s+dot\s+{_PART})+)\b"
)


def _join_domain(spoken: str) -> str | None:
  parts = [p.replace("▁", "").lower() for p in re.split(r"\s+dot\s+", spoken)]
  if parts[-1] not in KNOWN_TLDS:
    return None
  return ".".join(parts)


def _email_replacer(match) -> str:
  domain = _join_domain(match.group("domain"))
  if domain is None:
    return match.group(0)
  return f"{match.group('user').replace('▁', '')}@{domain}"


def _domain_replacer(match) -> str:
  domain = _join_domain(match.group(0))
  if domain is None:
    return match.group(0)
  return domain


def processor(text: str) -> str:
  """Rebuild verbalized URLs and emails.

  "google dot com dot k▁h" -> "google.com.kh",
  "example at g▁mail dot com" -> "example@gmail.com"
  """
  text = EMAIL_PATTERN.sub(_email_replacer, text)
  text = DOMAIN_PATTERN.sub(_domain_replacer, text)
  return text


__all__ = ["processor"]
