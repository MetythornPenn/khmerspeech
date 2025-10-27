import khmerspeech as ks

## Normalize
assert ks.normalize.processor("មិន\u200bឲ្យ") == "មិនឱ្យ"

## Phone Numbers
assert ks.phone_numbers.processor("010123123", chunk_size=2) == "0▁10▁12▁31▁23"
assert ks.phone_numbers.processor("010123123", chunk_size=3) == "0▁10▁123▁123"
assert ks.phone_numbers.processor("0961231234", chunk_size=3) == "0▁96▁123▁1234"

## URLs and emails
assert ks.urls.processor("example@gmail.com") == "example at g▁mail dot com"
assert ks.urls.processor("https://google.com") == "google dot com"
assert ks.urls.processor("http://google.com") == "google dot com"
assert ks.urls.processor("google.com") == "google dot com"
assert ks.urls.processor("google.gov.kh") == "google dot gov dot k▁h"
assert ks.urls.processor("google.com.kh") == "google dot com dot k▁h"

## Time
assert ks.datetime.time_processor("10:23AM") == "10 23▁A▁M"
assert ks.datetime.time_processor("10:23PM") == "10 23▁P▁M"
assert ks.datetime.time_processor("1:23PM") == "1 23▁P▁M"

## Date
assert ks.datetime.date_processor("2024-01-02") == "2024 01 02"
assert ks.datetime.date_processor("01-02-2034") == "01 02 2034"

## Hashtags
assert (
  ks.hashtags.processor("Hello world #this_will_remove hello") == "Hello world  hello"
)
assert ks.hashtags.processor("Hello world #លុប hello") == "Hello world  hello"
assert ks.hashtags.processor("Hello world #លុប1234 hello") == "Hello world  hello"

## ASCII Lines
assert ks.ascii_lines.processor("Remove --- asdasd") == "Remove  asdasd"
assert ks.ascii_lines.processor("Remove\n###\nasdasd") == "Remove\n\nasdasd"

## Cambodia License Plate
assert ks.license_plate.processor("1A 1234") == "1 A 12▁34"
assert ks.license_plate.processor("1A 4444") == "1 A ការ៉េ4"

## Number - Cardinals
assert ks.cardinals.processor("1234") == "មួយពាន់▁ពីររយ▁សាមសិបបួន"
assert ks.cardinals.processor("1") == "មួយ"
assert ks.cardinals.processor("1▁2") == "មួយ▁ពីរ"
assert ks.cardinals.processor("-1") == "ដក▁មួយ"
assert ks.cardinals.processor("10") == "ដប់"
assert ks.cardinals.processor("15") == "ដប់ប្រាំ"
assert ks.cardinals.processor("100") == "មួយរយ"
assert ks.cardinals.processor("10000") == "មួយម៉ឺន"
assert ks.cardinals.processor("10000.234") == "មួយម៉ឺន.ពីររយ▁សាមសិបបួន"
assert ks.cardinals.processor("-10000.234") == "ដក▁មួយម៉ឺន.ពីររយ▁សាមសិបបួន"
assert ks.cardinals.processor("-10000,234") == "ដក▁មួយម៉ឺន,ពីររយ▁សាមសិបបួន"

## Number - Decimals
assert ks.decimals.processor("123.324") == "មួយរយ▁ម្ភៃបី▁ចុច▁បីរយ▁ម្ភៃបួន"
assert ks.decimals.processor("123.001") == "មួយរយ▁ម្ភៃបី▁ចុច▁សូន្យ▁សូន្យ▁មួយ"
assert ks.decimals.processor("-123.0012") == "ដក▁មួយរយ▁ម្ភៃបី▁ចុច▁សូន្យ▁សូន្យ▁ដប់ពីរ"
assert ks.decimals.processor("-123,0012") == "ដក▁មួយរយ▁ម្ភៃបី▁ក្បៀស▁សូន្យ▁សូន្យ▁ដប់ពីរ"
assert (
  ks.decimals.processor("hello, world -123,0012")
  == "hello, world ដក▁មួយរយ▁ម្ភៃបី▁ក្បៀស▁សូន្យ▁សូន្យ▁ដប់ពីរ"
)

## Number - Ordinals
assert ks.ordinals.processor("5th") == "ទី▁ប្រាំ"
assert ks.ordinals.processor("3rd") == "ទី▁បី"
assert ks.ordinals.processor("1st") == "ទី▁មួយ"
assert ks.ordinals.processor("10th") == "ទី▁ដប់"
assert ks.ordinals.processor("10") == "10"

## Number - Currency
assert ks.currency.processor("$100.01") == "មួយរយដុល្លារ▁មួយសេន"
assert ks.currency.processor("$100") == "មួយរយ▁ដុល្លារ"
assert ks.currency.processor("100$") == "មួយរយ▁ដុល្លារ"
assert ks.currency.processor("100៛") == "មួយរយ▁រៀល"
assert ks.currency.processor("100.32៛") == "មួយរយចុចសាមសិបពីរ▁រៀល"
assert ks.currency.processor("100.0032៛") == "មួយរយចុចសាមសិបពីរ▁រៀល"
assert ks.currency.processor("asdasdas.asdas,d 100.0032៛") == "asdasdas.asdas,d មួយរយចុចសាមសិបពីរ▁រៀល"

## Parenthesis
assert ks.parenthesis.processor("Hello (this will be ignored) world") == "Hello world"


## Iteration Mark
def fake_tokenizer(_):
  return ["គាត់", "បាន", "ទៅ", "បន្តិច", "ម្ដង"]


assert (
  ks.repeater.processor("គាត់បានទៅបន្តិចម្ដងៗហើយ", tokenizer=fake_tokenizer)
  == "គាត់បានទៅបន្តិចម្ដង▁បន្តិចម្ដងហើយ"
)

## Quotes
assert ks.quotings.processor('lorem "content" lorem') == "lorem content lorem"

## Punctuations
assert (
  "".join(
    list(
      ks.punctuations.processor(
        'hello world "test test test"valuevalue"test test test"។។។។ valuevalueaaa'
      )
    )
  )
  == 'hello world "test test test"valuevalue"test test test"។ valuevalueaaa'
)

print("All tests case done")