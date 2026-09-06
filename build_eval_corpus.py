from datasets import load_dataset
import re
import unicodedata
from pathlib import Path

LANGS = {
    "eng": "sentence_eng_Latn",
    "hin": "sentence_hin_Deva",
    "kan": "sentence_kan_Knda",
    "tam": "sentence_tam_Taml",
}

CONFIGS = {
    "hin": "eng_Latn-hin_Deva",
    "kan": "eng_Latn-kan_Knda",
    "tam": "eng_Latn-tam_Taml",
}

def normalize(text):
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

datasets = {
    "eng": load_dataset(
        "facebook/flores",
        "eng_Latn-hin_Deva",
        split="devtest",
    )
}

for lang, config in CONFIGS.items():
    datasets[lang] = load_dataset(
        "facebook/flores",
        config,
        split="devtest",
    )

records = {}

for lang, ds in datasets.items():
    for row in ds:
        records.setdefault(row["id"], {})[lang] = normalize(
            row[LANGS[lang]]
        )

output_dir = Path("eval_corpus")
output_dir.mkdir(exist_ok=True)

for lang in LANGS:
    path = output_dir / f"{lang}.txt"
    with path.open("w", encoding="utf-8") as f:
        for idx in sorted(records):
            f.write(records[idx][lang] + "\n")

print("sentences:", len(records))

for lang in LANGS:
    print(lang, ":", len((output_dir / f"{lang}.txt").read_text(encoding="utf-8").splitlines()))