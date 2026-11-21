# Speech and Language Processing -- Assignment 2

This repository contains the complete deliverables, experimental pipelines, source code, and comprehensive reports for both parts of **Assignment 2**:

1. **Assignment 2a**: Forced Alignment using Montreal Forced Aligner (MFA)
2. **Assignment 2b**: Multimodal Emotion Recognition using Speech, Text, and Speech-Text Fusion

---

## Deliverables and Quick Links

| Deliverable | Description | PDF Location |
|---|---|---|
| **Assignment 2a Report** | Forced Alignment using Montreal Forced Aligner (MFA) | [`Assignment 2a/Report.pdf`](Assignment%202a/Report.pdf) |
| **Assignment 2b Report** | Multimodal Emotion Recognition (Speech, Text, Fusion) | [`Assignment 2b/Report.pdf`](Assignment%202b/Report.pdf) |
| **Combined Assignment 2 Report** | Unified Master Report encompassing Parts I & II | [`Report.pdf`](Report.pdf) |

- **GitHub Repository**: [https://github.com/savioshaju/Assignment_2](https://github.com/savioshaju/Assignment_2)
- **Trained Model Checkpoints & Artifacts (Google Drive)**: [https://drive.google.com/drive/folders/15YZdjhHsL-CtgAwFPwH1rJzM52Lnl5CG](https://drive.google.com/drive/folders/15YZdjhHsL-CtgAwFPwH1rJzM52Lnl5CG)

---

## Repository Architecture

```text
Assignment_2/
├── Report.pdf                            # Unified Assignment 2 Report
│
├── Assignment 2a/                        # Assignment 2a Directory
│   ├── wav/                              # Original speech audio recordings
│   ├── transcripts/                      # Original transcript files
│   ├── dict/                             # Stock & custom pronunciation dictionaries
│   ├── textgrid/                         # Generated output TextGrid alignment files
│   ├── scripts/                          # Alignment pipelines & evaluation scripts
│   ├── Report.pdf                        # Assignment 2a Report
│   └── README.md                         # Assignment 2a Documentation
│
└── Assignment 2b/                        # Assignment 2b Directory
    ├── models/                           # Pipeline implementations
    │   ├── speech_pipeline/              # Speech Emotion Recognition (SER)
    │   ├── text_pipeline/                # Text Emotion Recognition
    │   ├── fusion_pipeline/              # Multimodal Speech-Text Fusion
    │   ├── text_pipeline_DailyDialog/    # DailyDialog supporting text baseline
    │   └── fusion_pipeline_MELD/         # MELD supporting multimodal baseline
    ├── Results/                          # Experimental outputs, plots, and metrics
    │   ├── speech_pipeline/
    │   ├── text_pipeline/
    │   ├── fusion_pipeline/
    │   ├── text_pipeline_DailyDialog/
    │   ├── fusion_pipeline_MELD/
    │   ├── plots/
    │   └── all_model_variants_accuracy_table.csv
    ├── Report.pdf                        # Assignment 2b Report
    ├── requirements.txt                  # Python dependencies
    ├── setup.bat                         # Environment setup script
    └── README.md                         # Assignment 2b Documentation
```

---

## Assignment 2a: Forced Alignment using MFA

### Overview
Assignment 2a explores automated phonetic and lexical alignment using the **Montreal Forced Aligner (MFA)**, powered by Kaldi and Hidden Markov Models with Gaussian Mixture Models (HMM-GMM). The pipeline investigates acoustic mismatch, boundary precision, beam search dynamics, and pronunciation dictionary enrichment.

### Key Aspects
- **Corpora**: 
  - *Boston University Radio Speech Corpus (BU F2B)*: Fast-paced native broadcast speech (SPHERE container transcoded to 16 kHz mono RIFF WAV).
  - *ISLE Corpus*: Non-native English learner speech with prosodic variations and segmental substitutions.
- **Dictionary Curation**: Handled critical Out-of-Vocabulary (OOV) proper nouns (`DUKAKIS`, `HENNESSY`, `MAFFY`, `MELNICOVE`, `WBUR`) in `custom_us_arpa.dict`.
- **Experimental Configurations**: Evaluated six setups (Configs A–F) spanning baseline stock models, lexical enhancements, cross-corpus alignment, beam width adjustments (`--beam 100 --retry_beam 400`), phone inventories (Arpabet vs IPA), and Baum-Welch MLLR acoustic adaptation.
- **Documentation**: See [`Assignment 2a/README.md`](Assignment%202a/README.md).

---

## Assignment 2b: Multimodal Emotion Recognition

### Overview
Assignment 2b implements and compares three emotion recognition architectures across unimodal and multimodal settings:
1. **Speech Emotion Recognition (SER)**: 1D CNN + Bidirectional LSTM + Temporal Attention on Mel-spectrogram features.
2. **Text Emotion Recognition**: RoBERTa-base transformer fine-tuned on semantic transcriptions.
3. **Multimodal Speech-Text Fusion**: Dual-stream bidirectional cross-attention fusion mechanism with residual connections.

### Key Results Summary

| Pipeline | Dataset | Modality | Accuracy | Macro F1 | Status |
|---|---|---|---:|---:|---|
| **Speech SER** | TESS | Audio | **99.89%** | **99.89%** | Checkpoint Available |
| **Text SER** | TESS | Text | **14.29%** | **6.35%** | Checkpoint Available |
| **Multimodal Fusion SER (Custom)** | TESS | Audio + Text | **98.60%** | **98.60%** | Checkpoint Available |
| **Multimodal Fusion SER (Pretrained WavLM)** | TESS | Audio + Text | **99.68%** | — | Reference Benchmark |
| **Text SER (DailyDialog)** | DailyDialog | Text | **77.34%** | **46.49%** | Supporting Baseline |
| **Multimodal Fusion SER (MELD)** | MELD | Audio + Text | **59.50%** | **41.36%** | Supporting Baseline |

- **Documentation**: See [`Assignment 2b/README.md`](Assignment%202b/README.md).
