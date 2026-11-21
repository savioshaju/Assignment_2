#!/usr/bin/env python3
"""
build_ipa_dictionaries.py - Generate Compatible Standard and Custom IPA Dictionaries for Model B (english_mfa)
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DICT_DIR = BASE_DIR / "dict"
CORPUS_DIR = BASE_DIR / "corpus_normalized"

RAW_G2P_DICT = DICT_DIR / "custom_mfa_ipa.dict"
STANDARD_IPA_DICT = DICT_DIR / "english_mfa_standard.dict"
CUSTOM_IPA_DICT = DICT_DIR / "custom_mfa_ipa.dict"

OOVS = {"MAFFY", "MELNICOVE", "WBUR"}

CURATED_OOV_IPA = {
    "maffy": ["m æ f i"],
    "melnicove": ["m ɛ l n ɪ k ow v"],
    "wbur": ["d ʌ b ə l j uː b iː j uː ɑ ɹ"],
    "dukakis": ["d ʉ k ɑ k ɪ s"],
    "hennessy": ["h ɛ n ɪ s i"]
}


def main():
    print("Building compatible IPA dictionaries for Model B (english_mfa)...")

    # Read the raw G2P dictionary generated from corpus
    entries = {}
    with open(RAW_G2P_DICT, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                word, prons = parts[0].lower(), parts[1]
                entries.setdefault(word, []).append(prons)
            elif parts:
                p = line.strip().split()
                word, prons = p[0].lower(), " ".join(p[1:])
                entries.setdefault(word, []).append(prons)

    # 1. Build Standard IPA Dictionary (omitting true OOVs: MAFFY, MELNICOVE, WBUR)
    with open(STANDARD_IPA_DICT, "w", encoding="utf-8") as f:
        for word in sorted(entries.keys()):
            if word.upper() in OOVS:
                continue
            for pron in entries[word]:
                f.write(f"{word}\t{pron}\n")
    print(f"[OK] Created {STANDARD_IPA_DICT} (Standard IPA, OOVs omitted)")

    # 2. Build Custom Curated IPA Dictionary (including verified/curated OOVs)
    # Update curated pronunciations
    for word, prons in CURATED_OOV_IPA.items():
        entries[word] = prons

    with open(CUSTOM_IPA_DICT, "w", encoding="utf-8") as f:
        for word in sorted(entries.keys()):
            for pron in entries[word]:
                f.write(f"{word}\t{pron}\n")
    print(f"[OK] Created {CUSTOM_IPA_DICT} (Custom IPA, all OOVs resolved)")


if __name__ == "__main__":
    main()
