# All Model Variants Accuracy Comparison Table

This table aggregates the evaluation results across all model variants as required by the Assignment 2 task specification.

| Pipeline Variant | Modality | Dataset | Architecture | Test Accuracy | UAR | Macro F1 | Evaluation Protocol | Status |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :--- | :---: |
| **Speech Pipeline** | Audio | TESS | CNN-BiLSTM-Attention (Mel+Delta+MFCC) | **99.89%** | **99.89%** | **99.89%** | 5% Target-Speaker Adaptation | Trained Core Variant |
| **Text Pipeline** | Text | TESS | DistilBERT (`distilbert-base-uncased`) | **14.29%** | **14.29%** | **6.35%** | 5% Target-Speaker Adaptation *(1)* | Trained Core Variant |
| **Multimodal Fusion Pipeline** | Audio + Text | TESS | Custom CNN-BiLSTM-Attention + DistilBERT | **98.60%** | **98.60%** | **98.60%** | 5% Target-Speaker Adaptation | Trained Core Variant |
| **Text Pipeline (Supporting)** | Text | DailyDialog | RoBERTa (`roberta-base`) | **78.15%** | **59.92%** | **45.95%** | Standard Dialogue Split | Supporting Baseline |
| **Multimodal Fusion (Supporting)** | Audio + Text | MELD | CNN-BiLSTM-Attention + DistilBERT | **57.70%** | **42.24%** | **40.61%** | Class-Weighted Multi-speaker Split | Supporting Baseline |

*(1) Note on Text-Only Performance on TESS:* In TESS, identical carrier phrases (`"Say the word [word]"`) are spoken across all 7 emotions. Because carrier words contain zero emotional semantics, the text pipeline correctly reflects the random-chance baseline ($1/7 = 14.28\%$). The supporting DailyDialog experiment confirms the text architecture functions with high accuracy (78.15%) on emotionally expressive text.
