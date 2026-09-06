import argparse
import regex
import tiktoken
import unicodedata


def read_lines(path):
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            line = unicodedata.normalize("NFC", line)
            lines.append(line)
    return lines


def analyze(lines, encode):
    total_tokens = 0
    total_words = 0
    total_codepoints = 0
    total_graphemes = 0

    for line in lines:
        line = " ".join(line.split()).lower()

        total_tokens += len(encode.encode(line))
        total_words += len(line.split())
        total_codepoints += len(line)
        total_graphemes += len(regex.findall(r"\X", line))

    return (
        total_tokens / total_words,
        total_tokens / total_codepoints,
        total_tokens / total_graphemes,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", action="append", required=True)
    parser.add_argument("--tokenizer", default="gpt2")
    args = parser.parse_args()

    enc = tiktoken.get_encoding(args.tokenizer)

    for spec in args.corpus:
        lang, path = spec.split("=", 1)
        lines = read_lines(path)

        fertility, tok_codepoint, tok_grapheme = analyze(lines, enc)

        print(
            f"{lang:<8}"
            f"{fertility:>12.3f}"
            f"{tok_codepoint:>18.3f}"
            f"{tok_grapheme:>18.3f}"
        )


if __name__ == "__main__":
    main()