## KhmerSpeech

Khmer Speech Toolkit.


## Install

```shell
pip install khmerspeech
```

```python
import khmerspeech.normalize
import khmerspeech.phone_numbers
import khmerspeech.urls
import khmerspeech.datetime
import khmerspeech.hashtags
import khmerspeech.ascii_lines
import khmerspeech.license_plate
import khmerspeech.cardinals
import khmerspeech.decimals
import khmerspeech.ordinals
import khmerspeech.currency
import khmerspeech.parenthesis
import khmerspeech.repeater

## Normalize
assert khmerspeech.normalize.processor("មិន\u200bឲ្យ") == "មិនឱ្យ"

## Phone Numbers
assert khmerspeech.phone_numbers.processor("010123123", chunk_size=2) == "0▁10▁12▁31▁23"
assert khmerspeech.phone_numbers.processor("010123123", chunk_size=3) == "0▁10▁123▁123"
assert khmerspeech.phone_numbers.processor("0961231234", chunk_size=3) == "0▁96▁123▁1234"

## URLs and emails
assert khmerspeech.urls.processor("example@gmail.com") == "example at g▁mail dot com"
assert khmerspeech.urls.processor("https://google.com") == "google dot com"
assert khmerspeech.urls.processor("http://google.com") == "google dot com"
assert khmerspeech.urls.processor("google.com") == "google dot com"
assert khmerspeech.urls.processor("google.gov.kh") == "google dot gov dot k▁h"
assert khmerspeech.urls.processor("google.com.kh") == "google dot com dot k▁h"

## Time
assert khmerspeech.datetime.time_processor("10:23AM") == "10 23▁A▁M"
assert khmerspeech.datetime.time_processor("10:23PM") == "10 23▁P▁M"
assert khmerspeech.datetime.time_processor("1:23PM") == "1 23▁P▁M"

## Date
assert khmerspeech.datetime.date_processor("2024-01-02") == "2024 01 02"
assert khmerspeech.datetime.date_processor("01-02-2034") == "01 02 2034"

## Hashtags
assert (
  khmerspeech.hashtags.processor("Hello world #this_will_remove hello") == "Hello world  hello"
)
assert khmerspeech.hashtags.processor("Hello world #លុប hello") == "Hello world  hello"
assert khmerspeech.hashtags.processor("Hello world #លុប1234 hello") == "Hello world  hello"

## ASCII Lines
assert khmerspeech.ascii_lines.processor("Remove --- asdasd") == "Remove  asdasd"
assert khmerspeech.ascii_lines.processor("Remove\n###\nasdasd") == "Remove\n\nasdasd"

## Cambodia License Plate
assert khmerspeech.license_plate.processor("1A 1234") == "1 A 12▁34"
assert khmerspeech.license_plate.processor("1A 4444") == "1 A ការ៉េ4"

## Number - Cardinals
assert khmerspeech.cardinals.processor("1234") == "មួយពាន់▁ពីររយ▁សាមសិបបួន"
assert khmerspeech.cardinals.processor("1") == "មួយ"
assert khmerspeech.cardinals.processor("1▁2") == "មួយ▁ពីរ"
assert khmerspeech.cardinals.processor("-1") == "ដក▁មួយ"
assert khmerspeech.cardinals.processor("10") == "ដប់"
assert khmerspeech.cardinals.processor("15") == "ដប់ប្រាំ"
assert khmerspeech.cardinals.processor("100") == "មួយរយ"
assert khmerspeech.cardinals.processor("10000") == "មួយម៉ឺន"
assert khmerspeech.cardinals.processor("10000.234") == "មួយម៉ឺន.ពីររយ▁សាមសិបបួន"
assert khmerspeech.cardinals.processor("-10000.234") == "ដក▁មួយម៉ឺន.ពីររយ▁សាមសិបបួន"
assert khmerspeech.cardinals.processor("-10000,234") == "ដក▁មួយម៉ឺន,ពីររយ▁សាមសិបបួន"

## Number - Decimals
assert khmerspeech.decimals.processor("123.324") == "មួយរយ▁ម្ភៃបី▁ចុច▁បីរយ▁ម្ភៃបួន"
assert khmerspeech.decimals.processor("123.001") == "មួយរយ▁ម្ភៃបី▁ចុច▁សូន្យ▁សូន្យ▁មួយ"
assert khmerspeech.decimals.processor("-123.0012") == "ដក▁មួយរយ▁ម្ភៃបី▁ចុច▁សូន្យ▁សូន្យ▁ដប់ពីរ"
assert khmerspeech.decimals.processor("-123,0012") == "ដក▁មួយរយ▁ម្ភៃបី▁ក្បៀស▁សូន្យ▁សូន្យ▁ដប់ពីរ"

## Number - Ordinals
assert khmerspeech.ordinals.processor("5th") == "ទី▁ប្រាំ"
assert khmerspeech.ordinals.processor("3rd") == "ទី▁បី"
assert khmerspeech.ordinals.processor("1st") == "ទី▁មួយ"
assert khmerspeech.ordinals.processor("10th") == "ទី▁ដប់"
assert khmerspeech.ordinals.processor("10") == "10"

## Number - Currency
assert khmerspeech.currency.processor("$100.01") == "មួយរយដុល្លារ▁មួយសេន"
assert khmerspeech.currency.processor("$100") == "មួយរយ▁ដុល្លារ"
assert khmerspeech.currency.processor("100$") == "មួយរយដុល្លារ"
assert khmerspeech.currency.processor("100៛") == "មួយរយរៀល"
assert khmerspeech.currency.processor("100.32៛") == "មួយរយ▁ចុច▁សាមសិបពីររៀល"
assert khmerspeech.currency.processor("100.0032៛") == "មួយរយ▁ចុច▁សូន្យ▁សូន្យ▁សាមសិបពីររៀល"

## Parenthesis
assert khmerspeech.parenthesis.processor("Hello (this will be ignored) world") == "Hello world"


## Iteration Mark
def fake_tokenizer(_):
  return ["គាត់", "បាន", "ទៅ", "បន្តិច", "ម្ដង"]


assert (
  tha.repeater.processor("គាត់បានទៅបន្តិចម្ដងៗហើយ", tokenizer=fake_tokenizer)
  == "គាត់បានទៅបន្តិចម្ដង▁បន្តិចម្ដងហើយ"
)
```