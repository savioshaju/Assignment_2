# Assignment 2a: Forced Alignment Using Montreal Forced Aligner (MFA)

This project aligns speech audio with text transcripts using the Montreal Forced Aligner (MFA). It measures word and phoneme boundaries across native radio news and non-native English learner recordings.

## Project Links

- **GitHub Repository**: [https://github.com/savioshaju/Assignment_2](https://github.com/savioshaju/Assignment_2)
- **Assignment 2a Report**: [Report.pdf](Report.pdf)
- **Combined Assignment Report**: [../Report.pdf](../Report.pdf)

---

## Folder Structure

```text
Assignment 2a/
├── dict/
│   ├── custom_mfa_ipa.dict
│   ├── custom_us_arpa.dict
│   ├── english_mfa_standard.dict
│   └── english_us_arpa.dict
├── experiments/
│   ├── comparison/
│   │   ├── alignment_metrics.csv
│   │   ├── comparison_report.md
│   │   └── execution_logs/
│   │       ├── E1_model_A_standard.log
│   │       ├── E2_model_B_standard.log
│   │       ├── E3_model_A_custom.log
│   │       └── E4_model_B_custom.log
│   ├── model_A/
│   │   ├── custom_dictionary/
│   │   └── standard_dictionary/
│   ├── model_B/
│   │   ├── custom_dictionary/
│   │   └── standard_dictionary/
│   └── visualizations/
│       ├── experiment_evaluation_chart.png
│       ├── model_boundary_comparison.png
│       └── praat_alignment_representative.png
├── scripts/
│   ├── build_dictionary.py
│   ├── build_ipa_dictionaries.py
│   ├── compare.py
│   ├── plot_visualizations.py
│   ├── prepare_corpus.py
│   ├── run_experiments.py
│   ├── run_pipeline.bat
│   └── run_pipeline.sh
├── textgrid/
│   ├── config_B/
│   ├── F2BJRLP1.TextGrid
│   ├── F2BJRLP2.TextGrid
│   ├── F2BJRLP3.TextGrid
│   ├── ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid
│   ├── ISLE_SESS0131_BLOCKD02_02_sprt1.TextGrid
│   └── ISLE_SESS0131_BLOCKD02_03_sprt1.TextGrid
├── transcripts/
│   ├── F2BJRLP1.TXT
│   ├── F2BJRLP2.TXT
│   ├── F2BJRLP3.TXT
│   ├── ISLE_SESS0131_BLOCKD02_01_sprt1.txt
│   ├── ISLE_SESS0131_BLOCKD02_02_sprt1.txt
│   └── ISLE_SESS0131_BLOCKD02_03_sprt1.txt
├── wav/
│   ├── F2BJRLP1.wav
│   ├── F2BJRLP2.wav
│   ├── F2BJRLP3.wav
│   ├── ISLE_SESS0131_BLOCKD02_01_sprt1.wav
│   ├── ISLE_SESS0131_BLOCKD02_02_sprt1.wav
│   └── ISLE_SESS0131_BLOCKD02_03_sprt1.wav
├── Report.pdf
└── README.md
```

---

## Requirements

- **Montreal Forced Aligner (MFA):** v3.4.2
- **Python:** 3.10 or 3.11
- **Conda / Mamba:** Miniconda or Anaconda
- **FFmpeg:** 7.x
- **Praat:** 6.4
- **Python Packages:** `textgrid`, `praat-parselmouth`, `nltk`, `matplotlib`, `numpy`

---

## Step 1: Install MFA and Download Models

Run these commands to set up the environment and download the models:

```bash
conda create -n mfa -c conda-forge montreal-forced-aligner python=3.10 ffmpeg -y
conda activate mfa
mfa model download acoustic english_us_arpa
mfa model download acoustic english_mfa
pip install textgrid praat-parselmouth nltk matplotlib numpy
```

---

## Step 2: Prepare the Dataset

The Boston University radio files in `wav/` are saved in **NIST SPHERE** format (`NIST_1A` header). MFA requires standard 16 kHz 16-bit mono PCM WAV files.

Run the preparation script to convert the audio and generate matching `.lab` transcript files into `corpus_normalized/`:

```bash
python scripts/prepare_corpus.py
```

---

## Step 3: Dictionaries

The standard dictionaries lack five words: `DUKAKIS`, `HENNESSY`, `MAFFY`, `MELNICOVE`, and `WBUR`.
- Baseline pronunciations were extracted from CMUdict (`nltk.corpus.cmudict`).
- Missing proper names were phonetically transcribed.
- `WBUR` was manually corrected to spell out each letter name:
  - **Arpabet:** `D AH1 B AH0 L Y UW0 B IY1 Y UW1 AA1 R`
  - **IPA:** `d ʌ b ə l j uː b iː j uː ɑ ɹ`

All four pre-built dictionaries are already included in `dict/`:
- `dict/english_us_arpa.dict`: Standard CMU Arpabet (142 words)
- `dict/custom_us_arpa.dict`: Custom Arpabet with missing words (145 words)
- `dict/english_mfa_standard.dict`: Standard IPA (142 words)
- `dict/custom_mfa_ipa.dict`: Custom IPA with missing words (145 words)

No extra G2P download is needed to run the alignments. *(Optional) To rebuild the dictionary files:*
```bash
python scripts/build_dictionary.py
python scripts/build_ipa_dictionaries.py
```

---

## Step 4: Run the Alignment

### Experiment Matrix (E1 to E4)

| Exp | Acoustic Model | Phone Set | Dictionary | Purpose |
| :---: | :--- | :--- | :--- | :--- |
| **E1** | `english_us_arpa` | Arpabet | `dict/english_us_arpa.dict` | Baseline US Arpabet model with standard dictionary |
| **E2** | `english_mfa` | IPA | `dict/english_mfa_standard.dict` | Baseline multi-dialect IPA model with standard dictionary |
| **E3** | `english_us_arpa` | Arpabet | `dict/custom_us_arpa.dict` | Benchmark: US Arpabet model with custom dictionary |
| **E4** | `english_mfa` | IPA | `dict/custom_mfa_ipa.dict` | Multi-dialect IPA model with custom dictionary |

### Run All Experiments

Execute the automated runner to run all four experiments and log metrics. The script automatically detects `mfa` directly when your environment is active, or dispatches through Conda:

- **Windows:**
```powershell
python scripts/run_experiments.py --all
```

- **Linux / macOS:**
```bash
python3 scripts/run_experiments.py --all
```

*(Optional) To run a single experiment (e.g. E3):*
```bash
python scripts/run_experiments.py --experiment E3
```

---

## Step 5: Check the Output

### Open TextGrids in Praat
1. Open **Praat**.
2. Go to **Open** > **Read from file...** and select an audio file (e.g. `corpus_normalized/ISLE_SESS0131_BLOCKD02_01_sprt1.wav`).
3. Go to **Open** > **Read from file...** and select its TextGrid (e.g. `experiments/model_A/custom_dictionary/ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid`).
4. Select both objects together and click **View & Edit**.

### Run Comparison and Generate Plots

```bash
# Compare boundary metrics between Model A and Model B
python scripts/compare.py --ref experiments/model_A/custom_dictionary --test experiments/model_B/custom_dictionary --tier phones --out experiments/comparison/phone_comparison.csv

# Generate the three evaluation figures
python scripts/plot_visualizations.py
```

---

## Results Summary

Performance metrics from `experiments/comparison/alignment_metrics.csv`:

| Exp | Acoustic Model | Phone Set | Dictionary Used | Status | Success Rate | Run Time | Words Aligned |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **E1** | `english_us_arpa` | Arpabet | Standard (`english_us_arpa.dict`) | COMPLETED | 6 / 6 (100%) | 27.84 s | 246 |
| **E2** | `english_mfa` | IPA | Standard (`english_mfa_standard.dict`) | COMPLETED | 6 / 6 (100%) | 29.03 s | 246 |
| **E3** | `english_us_arpa` | Arpabet | Custom (`custom_us_arpa.dict`) | COMPLETED | 6 / 6 (100%) | 28.38 s | 246 |
| **E4** | `english_mfa` | IPA | Custom (`custom_mfa_ipa.dict`) | COMPLETED | 6 / 6 (100%) | 34.92 s | 246 |

**Best Setup:** **Experiment E3 (`english_us_arpa` with `custom_us_arpa.dict`)** performed best. It accurately aligns US broadcast speech, covers all proper nouns, and finishes faster than the IPA model.

---

## Troubleshooting

1. **Audio Header Error (`NIST_1A`):**
   - *Problem:* Audio files in `wav/` have NIST SPHERE headers. MFA crashes when reading them.
   - *Fix:* Run `python scripts/prepare_corpus.py` to transcode them to 16 kHz 16-bit mono RIFF WAV files.

2. **Single-Speaker Warning:**
   - *Problem:* MFA warns that jobs are reduced to 1 because all audio is in a single speaker folder.
   - *Fix:* This is expected. You can add `--single_speaker` to the MFA command to split utterances across cores.

3. **Ignored IPA Symbol in E4:**
   - *Problem:* MFA warns that 1 pronunciation was ignored due to an unrecognized phone symbol.
   - *Fix:* Ensure IPA symbols in `dict/custom_mfa_ipa.dict` match the standard phone set of `english_mfa`.

4. **Missing Python Modules:**
   - *Problem:* Running scripts gives `ModuleNotFoundError: No module named 'textgrid'`.
   - *Fix:* Install requirements with `pip install textgrid praat-parselmouth nltk matplotlib numpy`.
