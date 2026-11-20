"""Tests for khmerspeech.inverse_text_normalization (pytest or `python tests/test_inverse.py`)."""

import random

from khmerspeech import asr_normalize, inverse_normalize
from khmerspeech.inverse_text_normalization import (
  currency,
  datetime,
  numbers,
  ordinals,
  phone_numbers,
  urls,
)
from khmerspeech.text_normalization import cardinals as f_cardinals
from khmerspeech.text_normalization import currency as f_currency
from khmerspeech.text_normalization import decimals as f_decimals


def test_cardinals():
  assert numbers.processor("មួយ") == "1"
  assert numbers.processor("ដប់") == "10"
  assert numbers.processor("ដប់ប្រាំ") == "15"
  assert numbers.processor("មួយរយ") == "100"
  assert numbers.processor("មួយរយ▁ម្ភៃបី") == "123"
  assert numbers.processor("មួយពាន់▁ពីររយ▁សាមសិបបួន") == "1234"
  assert numbers.processor("មួយម៉ឺន") == "10000"
  assert numbers.processor("ប្រាំប៊ីលាន") == "5000000000"
  assert numbers.processor("ដក▁មួយរយ▁ម្ភៃបី") == "-123"


def test_separate_numbers_stay_separate():
  assert numbers.processor("មួយ▁ពីរ") == "1 2"
  assert numbers.processor("ដប់ មួយរយ") == "10 100"


def test_multiplier_groups():
  assert numbers.processor("មួយរយ▁ម្ភៃបីលាន▁បួនរយ▁ប្រាំ") == "123000405"


def test_decimals():
  assert numbers.processor("មួយរយ▁ម្ភៃបី▁ចុច▁សែសិបប្រាំ") == "123.45"
  assert numbers.processor("មួយរយ▁ម្ភៃបី▁ចុច▁សូន្យ▁សូន្យ▁មួយ") == "123.001"
  assert numbers.processor("ដក▁មួយរយ▁ម្ភៃបី▁ក្បៀស▁សូន្យ▁សូន្យ▁ដប់ពីរ") == "-123,0012"
  assert numbers.processor("សូន្យ▁ចុច▁ប្រាំ") == "0.5"


def test_does_not_touch_real_words():
  for text in ["រយៈពេល", "មួយរយៈ", "រាប់លាននាក់", "ទីក្រុងភ្នំពេញ", "ប្រាំបាទ"]:
    assert numbers.processor(text) == text
    assert ordinals.processor(text) == text


def test_currency():
  assert currency.processor("មួយរយដុល្លារ▁ម្ភៃប្រាំសេន") == "$100.25"
  assert currency.processor("មួយរយ▁ដុល្លារ") == "$100"
  assert currency.processor("មួយដុល្លារ▁ប្រាំសេន") == "$1.05"
  assert currency.processor("មួយរយ▁រៀល") == "100៛"


def test_ordinals():
  assert ordinals.processor("ទី▁ប្រាំ") == "ទី5"
  assert ordinals.processor("ចំណាត់ថ្នាក់ ទី▁ដប់ពីរ") == "ចំណាត់ថ្នាក់ ទី12"


def test_phone_numbers():
  assert phone_numbers.processor("0▁10▁123▁123") == "010123123"
  assert phone_numbers.processor("0 10 123 123") == "010123123"
  assert phone_numbers.processor("0 96 123 1234") == "0961231234"


def test_datetime():
  assert datetime.processor("10 23▁A▁M") == "10:23AM"
  assert datetime.processor("2024 1 2") == "2024-01-02"
  assert datetime.processor("1 2 2034") == "01-02-2034"


def test_urls():
  assert urls.processor("google dot com") == "google.com"
  assert urls.processor("google dot com dot k▁h") == "google.com.kh"
  assert urls.processor("example at g▁mail dot com") == "example@gmail.com"
  # "dot" followed by a non-TLD word must stay untouched
  assert urls.processor("connect the dot together") == "connect the dot together"


def test_roundtrip_cardinals():
  random.seed(7)
  values = list(range(0, 300)) + [random.randint(0, 10**9) for _ in range(500)]
  for n in values:
    spoken = f_cardinals.processor(str(n))
    assert numbers.processor(spoken) == str(n), f"{n} -> {spoken}"


def test_roundtrip_decimals():
  for n in ["123.45", "123.001", "-123.0012", "0.5", "3.14", "10.045"]:
    assert numbers.processor(f_decimals.processor(n)) == n


def test_roundtrip_currency():
  for s in ["$100.25", "$100", "100៛", "$1.05"]:
    assert currency.processor(f_currency.processor(s)) == s


def test_full_pipeline_roundtrip():
  raw = (
    "010123123 គិតថ្លៃ $100.25 នៅថ្ងៃទី 2024-01-02 វេលា 10:23AM "
    "ចូលតាម https://google.com.kh"
  )
  restored = inverse_normalize(asr_normalize(raw))
  assert restored == (
    "010123123 គិតថ្លៃ $100.25 នៅថ្ងៃទី 2024-01-02 វេលា 10:23AM "
    "ចូលតាម google.com.kh"
  )


if __name__ == "__main__":
  for name, fn in sorted(globals().items()):
    if name.startswith("test_") and callable(fn):
      fn()
      print(f"{name} passed")
  print("All inverse-normalization tests passed")
