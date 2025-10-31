import json
import regex as re
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

# from datasets import Audio, Dataset, DatasetDict, load_from_disk
from khmercut import tokenize as khmer_tokenize

from khmerspeech import (
  normalize,
  datetime as km_datetime,
  phone_numbers,
  currency,
  cardinals,
  decimals,
  urls,
  ordinals,
  dict_verbalize,
  repeater,
  punctuations,
  parenthesis
)

def segment_text(text: str) -> str:
    text = normalize.processor(text)
    text = phone_numbers.processor(text, chunk_size=3)
    text = km_datetime.date_processor(text)
    text = km_datetime.time_processor(text)
    text = urls.processor(text)
    text = repeater.processor(text)
    text = currency.processor(text)
    text = cardinals.processor(text)
    text = decimals.processor(text)
    text = ordinals.processor(text)
    text = punctuations.processor(text)
    text = dict_verbalize(text)
    
    try:
        tokens = khmer_tokenize(text)
        text = " ".join(tokens)
    except Exception:
        pass 
    # Normalize multiple spaces to a single space
    # text = re.sub(r"\s+", " ", text.strip())
    return text

segment_text('ការសិក្សាត្រូវមាន       ការព្យាយាម this  is the function for word segmentation!!! 010123123 គិតថ្លៃ $100.25 នៅថ្ងៃទី 2024-01-02 វេលា 10:23AM ចូលតាម https://google.com.kh')
# segment_text('ការសិក្សាត្រូវមានការព្យាយាម')