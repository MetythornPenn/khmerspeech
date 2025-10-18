# khmerspeech

KhmerSpeech is a text-normalization toolkit tailored for Khmer speech applications. It provides a set of focused processors that clean raw text and verbalize numbers, currencies, dates, URLs, and other tokens that regularly appear in transcripts.

This project is heavily inspired by, and builds on, the open-source [tha](https://github.com/seanghay/tha) repository created by Seanghay Yat; the modules here adapt his original work for Khmer-specific speech use cases.

## Requirements

- Python 3.8+ (tested with CPython)
- Bundled processors rely on `regex`, `phonenumbers`, `urlextract`, and `ftfy`. These are installed automatically when you install the package.

## Installation

### PyPI (planned)

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

## Usage

All processors live under the `khmerspeech` package. You can mix and match them to suit your pipeline.

```python
from khmerspeech import (
  normalize,
  datetime as km_datetime,
  phone_numbers,
  currency,
  cardinals,
  decimals,
)

raw = "010123123 គិតថ្លៃ $100.25 នៅថ្ងៃទី 2024-01-02 វេលា 10:23AM"

# 1. Clean up whitespace, punctuation, and Unicode issues.
clean = normalize.processor(raw)

# 2. Verbalize structured tokens.
clean = phone_numbers.processor(clean, chunk_size=3)
clean = km_datetime.date_processor(clean)
clean = km_datetime.time_processor(clean)
clean = currency.processor(clean)

print(clean)
# 0▁10▁123▁123 គិតថ្លៃ មួយរយដុល្លារ▁ម្ភៃប្រាំសេន នៅថ្ងៃទី 2024 01 02 វេលា 10 23▁A▁M

# Standalone helpers are also available:
print(cardinals.processor("1234"))          # មួយពាន់▁ពីររយ▁សាមសិបបួន
print(decimals.processor("-123.45"))        # ដក▁មួយរយ▁ម្ភៃបី▁ចុច▁សែសិបប្រាំ
```

Additional utilities include:

- `khmerspeech.urls.processor` – verbalize URLs and emails (`google.com.kh` → `google dot com dot k▁h`).
- `khmerspeech.hashtags.processor` – strip hashtags.
- `khmerspeech.parenthesis.processor` – remove content enclosed in parentheses or brackets.
- `khmerspeech.repeater.processor` – expand Khmer iteration marks (`ៗ`). Provide your own tokenizer that accepts Khmer strings.
- `khmerspeech.punctuations.processor` – split text into sentences while collapsing repeated punctuation.
- `khmerspeech.ascii_lines.processor` – drop ASCII art or divider lines.
- `khmerspeech.license_plate.processor` – normalize Cambodian vehicle license plates.
- `khmerspeech.ordinals.processor` – convert English ordinals (`5th`) into Khmer ordinal wording.

Refer to the source files under `khmerspeech/` for the full set of processors—each module is intentionally small and self-contained.

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
