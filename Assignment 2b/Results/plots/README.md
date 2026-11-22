# Consolidated Evaluation Plots

This directory aggregates all primary evaluation figures across the three model variants and supporting experiments as required by the Assignment 2 deliverables specification.

## Core Pipelines (TESS Dataset)
- `speech_confusion_matrix.png`: Normalized confusion matrix for Speech-only CNN-BiLSTM-Attention SER (99.89% Accuracy).
- `speech_training_curve.png`: Training/Validation Loss and Macro-F1 curve for Speech pipeline across epochs.
- `speech_pca_clusters.png`: 2D PCA emotional cluster separability from the **Temporal Modelling block** (CNN-BiLSTM-Attention).
- `text_confusion_matrix.png`: Confusion matrix for Text-only DistilBERT SER (14.29% Accuracy - random chance baseline on TESS carrier words).
- `text_training_curve.png`: Training/Validation Loss curve for Text DistilBERT pipeline.
- `text_pca_clusters.png`: 2D PCA representation space from the **Contextual Modelling block** (DistilBERT).
- `fusion_confusion_matrix.png`: Normalized confusion matrix for Multimodal Fusion SER (98.60% Accuracy).
- `fusion_training_curve.png`: Training/Validation Loss and Macro-F1 curve for Multimodal Fusion pipeline.
- `fusion_pca_clusters.png`: 2D PCA emotional cluster separability from **The Fusion block**.

## Supporting Benchmark Experiments
- `dailydialog_confusion_matrix.png`: RoBERTa text emotion classification on conversational DailyDialog dataset (77.34% Accuracy).
- `meld_confusion_matrix.png`: Multimodal emotion classification on noisy dialogue MELD dataset (59.50% Accuracy).
