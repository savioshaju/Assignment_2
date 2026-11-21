#!/usr/bin/env python3
"""
prepare_corpus.py - Stage and Normalize Speech Corpus for Montreal Forced Aligner (MFA)

Part of Assignment 2a: Forced Alignment using Montreal Forced Aligner (MFA).

Tasks performed:
1. Inspects raw audio files in Assignment 2a/wav.
2. Transcodes BU F2B files (NIST SPHERE container) into compliant 16 kHz 16-bit mono RIFF WAV.
3. Copies compliant ISLE files into the normalized corpus.
4. Normalizes transcripts from Assignment 2a/transcripts into single-line uppercase .lab files,
   stripping punctuation while preserving words and numbers.
5. Verifies audio-transcript pair consistency and reports audio durations.
"""

import os
import re
import shutil
import subprocess
import wave
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_WAV_DIR = BASE_DIR / "wav"
RAW_TRANSCRIPT_DIR = BASE_DIR / "transcripts"
NORMALIZED_CORPUS_DIR = BASE_DIR / "corpus_normalized"

FFMPEG_CMD = shutil.which("ffmpeg") or r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

# 6 Expected pairs
FILE_PAIRS = [
    ("F2BJRLP1.wav", "F2BJRLP1.TXT"),
    ("F2BJRLP2.wav", "F2BJRLP2.TXT"),
    ("F2BJRLP3.wav", "F2BJRLP3.TXT"),
    ("ISLE_SESS0131_BLOCKD02_01_sprt1.wav", "ISLE_SESS0131_BLOCKD02_01_sprt1.txt"),
    ("ISLE_SESS0131_BLOCKD02_02_sprt1.wav", "ISLE_SESS0131_BLOCKD02_02_sprt1.txt"),
    ("ISLE_SESS0131_BLOCKD02_03_sprt1.wav", "ISLE_SESS0131_BLOCKD02_03_sprt1.txt"),
]


def clean_text(text: str) -> str:
    """Normalize text to uppercase, single-spaced line without punctuation."""
    # Replace common dashes/hyphens and punctuation with spaces
    text = text.replace("-", " ").replace("—", " ").replace("–", " ")
    # Keep only alphanumeric and whitespace
    text = re.sub(r"[^\w\s]", " ", text)
    # Collapse multiple whitespaces and convert to uppercase
    text = " ".join(text.split()).upper()
    return text


def transcode_to_riff(src_wav: Path, dst_wav: Path):
    """Transcode any audio to 16 kHz 16-bit mono PCM RIFF WAV using ffmpeg."""
    cmd = [
        FFMPEG_CMD,
        "-y",
        "-i", str(src_wav),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(dst_wav)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg failed on {src_wav}: {res.stderr}")


def get_audio_info(wav_path: Path):
    """Read standard RIFF WAV header to get sample rate, channels, duration."""
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        ch = wf.getnchannels()
        nframes = wf.getnframes()
        dur = nframes / float(sr)
        sampwidth = wf.getsampwidth()
        return sr, ch, dur, sampwidth * 8


def main():
    print("=" * 70)
    print("Assignment 2a: Corpus Preparation & Normalization")
    print("=" * 70)

    NORMALIZED_CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Destination: {NORMALIZED_CORPUS_DIR}\n")

    summary_records = []

    for wav_name, txt_name in FILE_PAIRS:
        src_wav = RAW_WAV_DIR / wav_name
        src_txt = RAW_TRANSCRIPT_DIR / txt_name
        basename = Path(wav_name).stem

        dst_wav = NORMALIZED_CORPUS_DIR / f"{basename}.wav"
        dst_lab = NORMALIZED_CORPUS_DIR / f"{basename}.lab"

        if not src_wav.exists():
            raise FileNotFoundError(f"Missing raw audio: {src_wav}")
        if not src_txt.exists():
            raise FileNotFoundError(f"Missing transcript: {src_txt}")

        # Check raw header
        with open(src_wav, "rb") as f:
            header_bytes = f.read(16)
        is_nist = header_bytes.startswith(b"NIST_1A")

        if is_nist:
            print(f"[*] Transcoding NIST SPHERE -> RIFF: {wav_name}")
            transcode_to_riff(src_wav, dst_wav)
        else:
            print(f"[*] Standard RIFF WAV: {wav_name} (direct transcode/copy)")
            transcode_to_riff(src_wav, dst_wav)

        # Process transcript
        with open(src_txt, "r", encoding="utf-8", errors="replace") as f:
            raw_text = f.read()

        norm_text = clean_text(raw_text)
        with open(dst_lab, "w", encoding="utf-8") as f:
            f.write(norm_text + "\n")

        # Verify output WAV
        sr, ch, dur, bits = get_audio_info(dst_wav)
        words = norm_text.split()

        summary_records.append({
            "File": basename,
            "Type": "NIST SPHERE (transcoded)" if is_nist else "RIFF PCM",
            "Rate": f"{sr} Hz",
            "Channels": ch,
            "Bits": f"{bits}-bit",
            "Duration": f"{dur:.2f}s",
            "Word Count": len(words),
            "Transcript Preview": norm_text[:60] + ("..." if len(norm_text) > 60 else "")
        })

    print("\n" + "=" * 70)
    print("Corpus Preparation Summary:")
    print("=" * 70)
    for r in summary_records:
        print(f"[{r['File']}]")
        print(f"  Format:   {r['Type']} | {r['Rate']} | {r['Channels']}ch | {r['Bits']} | Duration: {r['Duration']}")
        print(f"  Words:    {r['Word Count']} words")
        print(f"  Text:     {r['Transcript Preview']}")
        print()

    print(f"Successfully staged {len(summary_records)} audio-transcript pairs in:")
    print(f"  {NORMALIZED_CORPUS_DIR}")


if __name__ == "__main__":
    main()
