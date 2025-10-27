# khmerspeech 

KhmerSpeech is a text-normalization toolkit tailored for Khmer speech applications. It provides a set of focused processors that clean raw text and verbalize numbers, currencies, dates, URLs, and other tokens that regularly appear in transcripts.

This project is heavily inspired by, and builds on, the open-source [tha](https://github.com/seanghay/tha) repository created by Seanghay Yat; the modules here adapt his original work for Khmer-specific speech use cases.

## Requirements

- Python 3.8+ (tested with CPython)
- Bundled processors rely on `regex`, `phonenumbers`, `urlextract`, and `ftfy`. These are installed automatically when you install the package.

## Installation

### PyPI 

The project will soon be published to PyPI. When it becomes available you will be able to install it with:

```bash
pip install khmerspeech
```

### From source

You can work directly from the repository today:

```bash
git clone https://github.com/MetythornPenn/khmerspeech
cd khmerspeech

# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

pip install -e .
```

This will install the package in editable mode along with its core dependencies.

## Quick start

All processors live under the `khmerspeech` namespace. Compose them to fit your pipeline:

```python
from khmerspeech import (
  normalize,
  datetime as km_datetime,
  phone_numbers,
  currency,
  cardinals,
  decimals,
  urls,
  dict_verbalize,
)

raw = "010123123 គិតថ្លៃ $100.25 នៅថ្ងៃទី 2024-01-02 វេលា 10:23AM ចូលតាម https://google.com.kh"

# 1. Normalize Khmer punctuation / Unicode issues.
clean = normalize.processor(raw)

# 2. Handle structured tokens.
clean = phone_numbers.processor(clean, chunk_size=3)
clean = km_datetime.date_processor(clean)
clean = km_datetime.time_processor(clean)
clean = currency.processor(clean)
clean = urls.processor(clean)

# 3. Expand dictionary-driven spellings / units.
clean = dict_verbalize(clean)

print(clean)
# 0▁10▁123▁123 គិតថ្លៃ មួយរយដុល្លារ▁ម្ភៃប្រាំសេន នៅថ្ងៃទី 2024 01 02 វេលា 10 23▁A▁M ចូលតាម google dot com dot k▁h

# Standalone helpers
print(cardinals.processor("1234"))   # មួយពាន់▁ពីររយ▁សាមសិបបួន
print(decimals.processor("-123.45")) # ដក▁មួយរយ▁ម្ភៃបី▁ចុច▁សែសិបប្រាំ
```

## Processors at a glance

| Module / helper | What it does | Example |
| --- | --- | --- |
| `normalize.processor` | Unicode cleanup, punctuation collapsing, whitespace normalization | `"មិន\u200bឲ្យ"` → `"មិនឱ្យ"` |
| `datetime.date_processor`, `datetime.time_processor` | Normalize numeric dates and clock times (AM/PM verbalized) | `"2024-01-02"` → `"2024 01 02"` |
| `phone_numbers.processor` | Chunk Khmer phone numbers while keeping carrier prefixes | `"010123123"` → `"0▁10▁123▁123"` |
| `currency.processor` | Verbalize USD / KHR amounts (supports `$`, `USD`, `៛`, `រៀល`) | `"$100.01"` → `"មួយរយដុល្លារ▁មួយសេន"` |
| `cardinals.processor` | Convert integers to Khmer wording | `"1234"` → `"មួយពាន់▁ពីររយ▁សាមសិបបួន"` |
| `decimals.processor` | Render decimal numbers with “ចុច/ក្បៀស” markers | `"123.001"` → `"មួយរយ▁ម្ភៃបី▁ចុច▁សូន្យ▁សូន្យ▁មួយ"` |
| `ordinals.processor` | Turn English ordinals (`1st`, `5th`, …) into Khmer | `"5th"` → `"ទី▁ប្រាំ"` |
| `urls.processor` | Verbalize URLs/emails, normalizing domain suffixes | `"google.com.kh"` → `"google dot com dot k▁h"` |
| `hashtags.processor` | Drop Khmer or Latin hashtags inline | `"Hello #ពិសោធន៍"` → `"Hello "` |
| `ascii_lines.processor` | Remove ASCII dividers / ruler lines | `"--- title ---"` → `" title "` |
| `license_plate.processor` | Reformat Cambodian license plates with syllable separators | `"1A 1234"` → `"1 A 12▁34"` |
| `parenthesis.processor` | Remove text inside `()` or `[]` | `"Hello (secret) world"` → `"Hello world"` |
| `repeater.processor` | Expand Khmer iteration mark `ៗ`; accepts custom tokenizers | `"បន្តិចម្ដងៗ"` → `"បន្តិចម្ដង▁បន្តិចម្ដង"` |
| `punctuations.processor` | Collapse repeated sentence-ending punctuation and enforce spacing | `"។។។"` → `"។ "` |
| `dict_verbalize` / `dictionary.processor` | Apply spelling, verbatim, and measurement-unit replacements from `dict/` TSVs | `"10 kg"` → `"10▁គីឡូក្រាម"` |

Each module is intentionally tiny—inspect the source under `khmerspeech/` if you need to tweak behaviour or build bespoke processors.

## Dictionary resources

The `dict/` folder ships pragmatic TSVs containing common spellings, pronunciations, and measurement units. `dict_verbalize` loads them at runtime:

```python
from khmerspeech import dict_verbalize

text = "100 km ឬ 10 kg"
print(dict_verbalize(text))
# 100▁គីឡូម៉ែត្រ ឬ 10▁គីឡូក្រាម
```

Add new terms by editing the TSV files and re-running your pipeline—no extra build step is required.

## Development

After installing in editable mode you can run the included assertions to spot regressions:

```bash
python tests.py
```

Code contributions are welcome. Please format new code with `ruff` or `black`, keep functions focused, and add tests for new processors.

## Acknowledgements

Credit goes to [Seanghay Yat](https://github.com/seanghay) for the original [tha](https://github.com/seanghay/tha) project, released under the MIT license. KhmerSpeech reuses and extends his processors to fit Khmer speech-normalization needs.

## License

khmerspeech is distributed under the Apache License 2.0. See the `LICENSE` file for the full text.
