#!/usr/bin/env bash
# run_pipeline.sh - MFA Forced Alignment Pipeline Runner for Assignment 2a
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

CORPUS_DIR="$BASE_DIR/corpus_normalized"
DICT_DIR="$BASE_DIR/dict"
OUTPUT_DIR="$BASE_DIR/textgrid"

STOCK_DICT="$DICT_DIR/english_us_arpa.dict"
CUSTOM_DICT="$DICT_DIR/custom_us_arpa.dict"
ACOUSTIC_MODEL="english_us_arpa"

mkdir -p "$OUTPUT_DIR/config_A"
mkdir -p "$OUTPUT_DIR/config_B"
mkdir -p "$OUTPUT_DIR/config_D"

echo "======================================================================"
echo "Assignment 2a: Montreal Forced Aligner Pipeline Execution"
echo "======================================================================"

# Step 1: Preprocessing & Dictionary Verification
python "$SCRIPT_DIR/prepare_corpus.py"
python "$SCRIPT_DIR/build_dictionary.py"

# Step 2: Config A - Baseline Stock Dictionary
echo ""
echo "[*] Running Config A: Stock english_us_arpa dictionary..."
mfa align "$CORPUS_DIR" "$STOCK_DICT" "$ACOUSTIC_MODEL" "$OUTPUT_DIR/config_A" --clean --overwrite || true

# Step 3: Config B - Custom Curated Dictionary (Resolving OOVs)
echo ""
echo "[*] Running Config B: Custom dictionary (resolving OOVs)..."
mfa align "$CORPUS_DIR" "$CUSTOM_DICT" "$ACOUSTIC_MODEL" "$OUTPUT_DIR/config_B" --clean --overwrite

# Step 4: Config D - Wide Beam Decoding
echo ""
echo "[*] Running Config D: Custom dictionary with Wide Beam (beam=100, retry_beam=400)..."
mfa align "$CORPUS_DIR" "$CUSTOM_DICT" "$ACOUSTIC_MODEL" "$OUTPUT_DIR/config_D" --beam 100 --retry_beam 400 --clean --overwrite

# Step 5: Copy primary results (Config B) to main textgrid folder
cp "$OUTPUT_DIR/config_B/"*.TextGrid "$OUTPUT_DIR/"

echo ""
echo "======================================================================"
echo "MFA Pipeline Finished Successfully!"
echo "Generated TextGrids in: $OUTPUT_DIR"
echo "======================================================================"
