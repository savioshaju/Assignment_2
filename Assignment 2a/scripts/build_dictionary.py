

from pathlib import Path
import nltk
from nltk.corpus import cmudict

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus_normalized"
DICT_DIR = BASE_DIR / "dict"

# Expert phonetic transcriptions for Out-of-Vocabulary proper nouns & acronyms
OOV_PRONUNCIATIONS = {
    "MAFFY": ["M", "AE1", "F", "IY0"],
    "MELNICOVE": ["M", "EH1", "L", "N", "IH0", "K", "OW0", "V"],
    "WBUR": ["D", "AH1", "B", "AH0", "L", "Y", "UW0", "B", "IY1", "Y", "UW1", "AA1", "R"],
}


def main():
    print("=" * 70)
    print("Assignment 2a: Pronunciation Dictionary Construction & OOV Curation")
    print("=" * 70)

    DICT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        cmu = cmudict.dict()
    except LookupError:
        nltk.download("cmudict")
        cmu = cmudict.dict()

    # 1. Gather all words from normalized .lab files
    all_words = set()
    for lab_file in sorted(CORPUS_DIR.glob("*.lab")):
        text = lab_file.read_text(encoding="utf-8").strip()
        all_words.update(text.split())

    words_sorted = sorted(all_words)
    print(f"Total Unique Corpus Words: {len(words_sorted)}")

    baseline_dict = {}
    custom_dict = {}
    oov_found = []

    for word in words_sorted:
        w_lower = word.lower()
        if w_lower in cmu:
            # Use primary CMU Arpabet pronunciation
            phones = cmu[w_lower][0]
            baseline_dict[word] = " ".join(phones)
            custom_dict[word] = " ".join(phones)
        else:
            oov_found.append(word)
            if word in OOV_PRONUNCIATIONS:
                custom_dict[word] = " ".join(OOV_PRONUNCIATIONS[word])
            else:
                raise ValueError(f"Unhandled OOV word: {word}")

    print(f"\n[1] Baseline In-Vocabulary Words: {len(baseline_dict)}")
    print(f"[2] Out-of-Vocabulary (OOV) Words ({len(oov_found)}): {oov_found}")
    for oov_w in oov_found:
        print(f"    - {oov_w}: {custom_dict[oov_w]}")

    # Write baseline dictionary
    stock_dict_path = DICT_DIR / "english_us_arpa.dict"
    with open(stock_dict_path, "w", encoding="utf-8") as f:
        for w in sorted(baseline_dict.keys()):
            f.write(f"{w} {baseline_dict[w]}\n")

    # Write custom curated dictionary
    custom_dict_path = DICT_DIR / "custom_us_arpa.dict"
    with open(custom_dict_path, "w", encoding="utf-8") as f:
        for w in sorted(custom_dict.keys()):
            f.write(f"{w} {custom_dict[w]}\n")

    print(f"\nSuccessfully generated dictionaries:")
    print(f"  - Baseline: {stock_dict_path} ({len(baseline_dict)} entries)")
    print(f"  - Curated:  {custom_dict_path} ({len(custom_dict)} entries)")


if __name__ == "__main__":
    main()
