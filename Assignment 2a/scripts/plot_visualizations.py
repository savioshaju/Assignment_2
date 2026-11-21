#!/usr/bin/env python3
"""
plot_visualizations.py - Focused Visualizations for Assignment 2a

Generates strictly the three required visual outputs:
1. praat_alignment_representative.png:
   Representative Praat alignment showing waveform, spectrogram, word tier, and phoneme tier.
2. model_boundary_comparison.png:
   Acoustic-model comparison visualization showing word/phoneme boundary differences using identical audio.
3. experiment_evaluation_chart.png:
   Compact evaluation chart comparing E1-E4 across completion rate, failures, and execution time.

Outputs are saved in:
- Assignment 2a/experiments/visualizations/
- Assignment 2a/Report/images/ (for LaTeX document integration)
"""

import csv
import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import parselmouth
import textgrid

BASE_DIR = Path(__file__).resolve().parent.parent
EXP_DIR = BASE_DIR / "experiments"
CORPUS_DIR = BASE_DIR / "corpus_normalized"
VIS_DIR = EXP_DIR / "visualizations"
REPORT_IMG_DIR = BASE_DIR / "Report" / "images"

VIS_DIR.mkdir(parents=True, exist_ok=True)
REPORT_IMG_DIR.mkdir(parents=True, exist_ok=True)


def plot_representative_praat_alignment():
    """Figure 1: Representative Praat alignment with waveform, spectrogram, words, and phones."""
    wav_path = CORPUS_DIR / "ISLE_SESS0131_BLOCKD02_01_sprt1.wav"
    tg_path = EXP_DIR / "model_A" / "custom_dictionary" / "ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid"

    if not wav_path.exists() or not tg_path.exists():
        print(f"[WARN] Files missing for representative alignment.")
        return

    snd = parselmouth.Sound(str(wav_path))
    tg = textgrid.TextGrid.fromFile(str(tg_path))

    # Time window: 0.5s to 2.4s ("I said white not bait")
    t_min, t_max = 0.5, 2.4
    snd_part = snd.extract_part(from_time=t_min, to_time=t_max, preserve_times=True)

    fig = plt.figure(figsize=(11, 6.5), dpi=300)
    gs = fig.add_gridspec(4, 1, height_ratios=[1.2, 2.8, 0.8, 1.0], hspace=0.15)

    # 1. Waveform
    ax_wave = fig.add_subplot(gs[0])
    times = snd_part.xs()
    samples = snd_part.values[0]
    ax_wave.plot(times, samples, color="#1e3a8a", lw=0.8)
    ax_wave.set_xlim(t_min, t_max)
    ax_wave.set_ylabel("Amplitude", fontsize=9, fontweight="bold")
    ax_wave.tick_params(labelbottom=False, labelsize=8)
    ax_wave.grid(True, alpha=0.3, ls=":")
    ax_wave.set_title("Representative Praat Forced Alignment (Model A + Custom Dictionary)", fontsize=11, fontweight="bold", pad=8)

    # 2. Spectrogram
    ax_spec = fig.add_subplot(gs[1])
    spectrogram = snd_part.to_spectrogram(window_length=0.005, maximum_frequency=5000.0)
    sg_vals = 10 * np.log10(spectrogram.values + 1e-10)
    sg_vals = np.clip(sg_vals, np.max(sg_vals) - 45, np.max(sg_vals))
    ax_spec.imshow(sg_vals, origin="lower", extent=[spectrogram.xmin, spectrogram.xmax, spectrogram.ymin, spectrogram.ymax], aspect="auto", cmap="Greys")
    ax_spec.set_ylim(0, 5000)
    ax_spec.set_xlim(t_min, t_max)
    ax_spec.set_ylabel("Frequency (Hz)", fontsize=9, fontweight="bold")
    ax_spec.tick_params(labelbottom=False, labelsize=8)

    # Helper function to draw tiers
    def draw_tier(ax, tier, label_name, bg_color="#e0f2fe", text_color="#0369a1"):
        ax.set_xlim(t_min, t_max)
        ax.set_ylim(0, 1)
        ax.set_ylabel(label_name, fontsize=8.5, fontweight="bold", rotation=0, labelpad=42, va="center")
        ax.tick_params(left=False, labelleft=False, labelbottom=False)
        for interval in tier:
            xmin = max(interval.minTime, t_min)
            xmax = min(interval.maxTime, t_max)
            if xmax > t_min and xmin < t_max:
                ax.axvline(xmin, color="#334155", lw=1.0)
                mark = interval.mark.strip()
                if mark:
                    ax.axvspan(xmin, xmax, facecolor=bg_color, alpha=0.75, edgecolor="#334155", lw=0.8)
                    mid = (xmin + xmax) / 2
                    if t_min <= mid <= t_max:
                        ax.text(mid, 0.5, mark, ha="center", va="center", fontsize=9.5, fontweight="bold", color=text_color)
        ax.axvline(t_max, color="#334155", lw=1.0)

    # 3. Words Tier
    ax_w = fig.add_subplot(gs[2])
    draw_tier(ax_w, tg.tiers[0], "Words\nTier", bg_color="#e0e7ff", text_color="#312e81")

    # 4. Phones Tier
    ax_p = fig.add_subplot(gs[3])
    draw_tier(ax_p, tg.tiers[1], "Phones\nTier\n(Arpabet)", bg_color="#ecfeff", text_color="#0e7490")
    ax_p.tick_params(labelbottom=True, labelsize=8.5)
    ax_p.set_xlabel("Time (seconds)", fontsize=9, fontweight="bold")

    out_vis = VIS_DIR / "praat_alignment_representative.png"
    plt.savefig(out_vis, bbox_inches="tight", dpi=300)
    plt.close()
    shutil.copy(out_vis, REPORT_IMG_DIR / "praat_alignment_representative.png")
    print(f"[OK] Representative Praat alignment saved to: {out_vis}")


def plot_acoustic_model_comparison():
    """Figure 2: Acoustic-model boundary comparison using identical audio."""
    wav_path = CORPUS_DIR / "ISLE_SESS0131_BLOCKD02_01_sprt1.wav"
    tg_a_path = EXP_DIR / "model_A" / "custom_dictionary" / "ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid"
    tg_b_path = EXP_DIR / "model_B" / "custom_dictionary" / "ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid"

    if not wav_path.exists() or not tg_a_path.exists() or not tg_b_path.exists():
        print(f"[WARN] Files missing for acoustic model comparison.")
        return

    snd = parselmouth.Sound(str(wav_path))
    tg_a = textgrid.TextGrid.fromFile(str(tg_a_path))
    tg_b = textgrid.TextGrid.fromFile(str(tg_b_path))

    t_min, t_max = 0.8, 2.4
    snd_part = snd.extract_part(from_time=t_min, to_time=t_max, preserve_times=True)

    fig = plt.figure(figsize=(11, 7.5), dpi=300)
    gs = fig.add_gridspec(6, 1, height_ratios=[1.1, 2.4, 0.7, 0.9, 0.7, 0.9], hspace=0.12)

    # Waveform
    ax_wave = fig.add_subplot(gs[0])
    times = snd_part.xs()
    samples = snd_part.values[0]
    ax_wave.plot(times, samples, color="#2b5c8f", lw=0.8)
    ax_wave.set_xlim(t_min, t_max)
    ax_wave.set_ylabel("Amplitude", fontsize=8.5, fontweight="bold")
    ax_wave.tick_params(labelbottom=False, labelsize=8)
    ax_wave.grid(True, alpha=0.3, ls=":")
    ax_wave.set_title("Acoustic-Model Alignment Boundary Comparison (Identical Audio Signal)", fontsize=10.5, fontweight="bold", pad=8)

    # Spectrogram
    ax_spec = fig.add_subplot(gs[1])
    spectrogram = snd_part.to_spectrogram(window_length=0.005, maximum_frequency=5000.0)
    sg_vals = 10 * np.log10(spectrogram.values + 1e-10)
    sg_vals = np.clip(sg_vals, np.max(sg_vals) - 45, np.max(sg_vals))
    ax_spec.imshow(sg_vals, origin="lower", extent=[spectrogram.xmin, spectrogram.xmax, spectrogram.ymin, spectrogram.ymax], aspect="auto", cmap="Greys")
    ax_spec.set_ylim(0, 5000)
    ax_spec.set_xlim(t_min, t_max)
    ax_spec.set_ylabel("Frequency (Hz)", fontsize=8.5, fontweight="bold")
    ax_spec.tick_params(labelbottom=False, labelsize=8)

    def draw_tier(ax, tier, label_name, bg_color="#eef3f8", text_color="#1a365d"):
        ax.set_xlim(t_min, t_max)
        ax.set_ylim(0, 1)
        ax.set_ylabel(label_name, fontsize=8, fontweight="bold", rotation=0, labelpad=48, va="center")
        ax.tick_params(left=False, labelleft=False, labelbottom=False)
        for interval in tier:
            xmin = max(interval.minTime, t_min)
            xmax = min(interval.maxTime, t_max)
            if xmax > t_min and xmin < t_max:
                ax.axvline(xmin, color="#475569", lw=0.9, ls="-")
                mark = interval.mark.strip()
                if mark:
                    ax.axvspan(xmin, xmax, facecolor=bg_color, alpha=0.75, edgecolor="#475569", lw=0.8)
                    mid = (xmin + xmax) / 2
                    if t_min <= mid <= t_max:
                        ax.text(mid, 0.5, mark, ha="center", va="center", fontsize=8.5, fontweight="bold", color=text_color)
        ax.axvline(t_max, color="#475569", lw=0.9, ls="-")

    # Model A Words
    ax_w_a = fig.add_subplot(gs[2])
    draw_tier(ax_w_a, tg_a.tiers[0], "Model A\nWords", bg_color="#e0e7ff", text_color="#1e3a8a")

    # Model A Phones (Arpabet)
    ax_p_a = fig.add_subplot(gs[3])
    draw_tier(ax_p_a, tg_a.tiers[1], "Model A\nPhones\n(Arpabet)", bg_color="#ecfeff", text_color="#0369a1")

    # Model B Words
    ax_w_b = fig.add_subplot(gs[4])
    draw_tier(ax_w_b, tg_b.tiers[0], "Model B\nWords", bg_color="#fdf2f8", text_color="#831843")

    # Model B Phones (IPA)
    ax_p_b = fig.add_subplot(gs[5])
    draw_tier(ax_p_b, tg_b.tiers[1], "Model B\nPhones\n(IPA)", bg_color="#fff1f2", text_color="#9f1239")
    ax_p_b.tick_params(labelbottom=True, labelsize=8)
    ax_p_b.set_xlabel("Time (seconds)", fontsize=8.5, fontweight="bold")

    out_vis = VIS_DIR / "model_boundary_comparison.png"
    plt.savefig(out_vis, bbox_inches="tight", dpi=300)
    plt.close()
    shutil.copy(out_vis, REPORT_IMG_DIR / "model_boundary_comparison.png")
    print(f"[OK] Model boundary comparison saved to: {out_vis}")


def plot_experiment_evaluation_chart():
    """Figure 3: Compact chart comparing E1-E4 across completion rate, failures, and execution time."""
    metrics_csv = EXP_DIR / "comparison" / "alignment_metrics.csv"
    if not metrics_csv.exists():
        print(f"[WARN] Metrics CSV not found: {metrics_csv}")
        return

    exp_data = []
    with open(metrics_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            exp_data.append(row)

    if not exp_data:
        print("[WARN] No data in metrics CSV.")
        return

    exps = [r["Experiment"] for r in exp_data]
    completion_rates = [(int(r["Success_Count"]) / 6.0) * 100.0 for r in exp_data]
    failures = [int(r["Fail_Count"]) for r in exp_data]
    durations = [float(r["Duration_Sec"]) for r in exp_data]
    labels = [
        "E1: Model A\n(Standard Arpa)",
        "E2: Model B\n(Standard IPA)",
        "E3: Model A\n(Custom Arpa)",
        "E4: Model B\n(Custom IPA)"
    ]

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), dpi=300)

    # 1. Alignment Completion Rate (%)
    colors = ["#2563eb", "#059669", "#4f46e5", "#0d9488"]
    bars1 = axes[0].bar(labels, completion_rates, color=colors, width=0.55, edgecolor="#1e293b", lw=0.8)
    axes[0].set_title("Alignment Completion Rate (%)", fontsize=10, fontweight="bold", pad=8)
    axes[0].set_ylabel("Completion Rate (%)", fontsize=8.5, fontweight="bold")
    axes[0].set_ylim(0, 120)
    axes[0].grid(axis="y", ls=":", alpha=0.5)
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2, yval + 2, f"{int(yval)}% (6/6)", ha="center", va="bottom", fontsize=8, fontweight="bold")

    # 2. Number of Alignment Failures
    bars2 = axes[1].bar(labels, failures, color="#ef4444", width=0.55, edgecolor="#1e293b", lw=0.8)
    axes[1].set_title("Alignment Failures (Count)", fontsize=10, fontweight="bold", pad=8)
    axes[1].set_ylabel("Failed Recordings", fontsize=8.5, fontweight="bold")
    axes[1].set_ylim(0, 3)
    axes[1].grid(axis="y", ls=":", alpha=0.5)
    for bar in bars2:
        axes[1].text(bar.get_x() + bar.get_width() / 2, 0.1, "0 failures", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#15803d")

    # 3. Execution Time (Seconds)
    bars3 = axes[2].bar(labels, durations, color=colors, width=0.55, edgecolor="#1e293b", lw=0.8)
    axes[2].set_title("Alignment Execution Time (s)", fontsize=10, fontweight="bold", pad=8)
    axes[2].set_ylabel("Seconds", fontsize=8.5, fontweight="bold")
    axes[2].set_ylim(0, max(durations) * 1.25)
    axes[2].grid(axis="y", ls=":", alpha=0.5)
    for bar in bars3:
        yval = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width() / 2, yval + 0.8, f"{yval:.1f}s", ha="center", va="bottom", fontsize=8, fontweight="bold")

    for ax in axes:
        ax.tick_params(axis="x", labelsize=7.5)
        ax.tick_params(axis="y", labelsize=8)

    plt.suptitle("Assignment 2a: Experimental Evaluation of Multiple Acoustic Models (E1 - E4)", fontsize=11, fontweight="bold", y=1.03)
    plt.tight_layout()

    out_vis = VIS_DIR / "experiment_evaluation_chart.png"
    plt.savefig(out_vis, bbox_inches="tight", dpi=300)
    plt.close()
    shutil.copy(out_vis, REPORT_IMG_DIR / "experiment_evaluation_chart.png")
    print(f"[OK] Experiment evaluation chart saved to: {out_vis}")


if __name__ == "__main__":
    plot_representative_praat_alignment()
    plot_acoustic_model_comparison()
    plot_experiment_evaluation_chart()
