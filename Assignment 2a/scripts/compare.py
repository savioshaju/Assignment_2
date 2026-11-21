
import argparse
import csv
from pathlib import Path
import numpy as np
import textgrid


def load_intervals(tg_path: Path, tier_name: str = "phones"):
    """Extract (label, xmin, xmax) tuples from a specific TextGrid tier."""
    tg = textgrid.TextGrid.fromFile(str(tg_path))
    tier = None
    for t in tg.tiers:
        if t.name.lower() == tier_name.lower():
            tier = t
            break
    if tier is None:
        raise ValueError(f"Tier '{tier_name}' not found in {tg_path}")

    intervals = []
    for interval in tier:
        label = interval.mark.strip()
        intervals.append({
            "label": label,
            "xmin": float(interval.minTime),
            "xmax": float(interval.maxTime),
            "dur": float(interval.maxTime) - float(interval.minTime)
        })
    return intervals


def evaluate_boundaries(ref_intervals, test_intervals):
    """
    Compute boundary errors between reference and test intervals.
    Matches non-empty intervals by label sequence order.
    """
    ref_clean = [i for i in ref_intervals if i["label"] != ""]
    test_clean = [i for i in test_intervals if i["label"] != ""]

    matched_count = min(len(ref_clean), len(test_clean))
    start_errors = []
    end_errors = []

    for i in range(matched_count):
        r = ref_clean[i]
        t = test_clean[i]
        start_errors.append(abs(t["xmin"] - r["xmin"]))
        end_errors.append(abs(t["xmax"] - r["xmax"]))

    all_errors = np.array(start_errors + end_errors) if matched_count > 0 else np.array([0.0])

    mae_ms = float(np.mean(all_errors) * 1000.0)
    rmse_ms = float(np.sqrt(np.mean(all_errors ** 2)) * 1000.0)

    pct_10ms = float(np.mean(all_errors <= 0.010) * 100.0)
    pct_20ms = float(np.mean(all_errors <= 0.020) * 100.0)
    pct_50ms = float(np.mean(all_errors <= 0.050) * 100.0)

    return {
        "matched_intervals": matched_count,
        "ref_intervals": len(ref_clean),
        "test_intervals": len(test_clean),
        "mae_ms": mae_ms,
        "rmse_ms": rmse_ms,
        "pct_10ms": pct_10ms,
        "pct_20ms": pct_20ms,
        "pct_50ms": pct_50ms,
    }


def compare_directories(ref_dir: Path, test_dir: Path, tier_name: str = "phones"):
    ref_files = sorted(ref_dir.glob("*.TextGrid"))
    test_files = sorted(test_dir.glob("*.TextGrid"))

    test_dict = {f.stem: f for f in test_files}

    file_results = []
    for rf in ref_files:
        stem = rf.stem
        if stem in test_dict:
            tf = test_dict[stem]
            ref_intervals = load_intervals(rf, tier_name=tier_name)
            test_intervals = load_intervals(tf, tier_name=tier_name)
            metrics = evaluate_boundaries(ref_intervals, test_intervals)
            metrics["filename"] = stem
            metrics["corpus"] = "BU_F2B" if "F2B" in stem else "ISLE"
            file_results.append(metrics)

    return file_results


def main():
    parser = argparse.ArgumentParser(description="Evaluate MFA TextGrid alignment accuracy")
    parser.add_argument("--ref", type=str, required=True, help="Path to reference/gold TextGrid directory")
    parser.add_argument("--test", type=str, required=True, help="Path to test TextGrid directory")
    parser.add_argument("--tier", type=str, default="phones", choices=["phones", "words"], help="Tier to evaluate")
    parser.add_argument("--out", type=str, default=None, help="Path to output summary CSV")
    args = parser.parse_args()

    ref_dir = Path(args.ref)
    test_dir = Path(args.test)

    print("=" * 70)
    print(f"TextGrid Boundary Evaluation: {args.tier.upper()} Tier")
    print(f"Reference: {ref_dir}")
    print(f"Test:      {test_dir}")
    print("=" * 70)

    results = compare_directories(ref_dir, test_dir, tier_name=args.tier)

    if not results:
        print("[!] No matching TextGrid pairs found.")
        return

    print(f"\n{'File':<36} | {'MAE (ms)':<9} | {'<=10ms':<8} | {'<=20ms':<8} | {'<=50ms':<8}")
    print("-" * 78)
    for r in results:
        print(f"{r['filename']:<36} | {r['mae_ms']:>7.2f}ms | {r['pct_10ms']:>6.1f}% | {r['pct_20ms']:>6.1f}% | {r['pct_50ms']:>6.1f}%")

    all_mae = [r["mae_ms"] for r in results]
    all_10 = [r["pct_10ms"] for r in results]
    all_20 = [r["pct_20ms"] for r in results]
    all_50 = [r["pct_50ms"] for r in results]

    print("-" * 78)
    print(f"{'OVERALL MEAN':<36} | {np.mean(all_mae):>7.2f}ms | {np.mean(all_10):>6.1f}% | {np.mean(all_20):>6.1f}% | {np.mean(all_50):>6.1f}%")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            writer.writeheader()
            writer.writerows(results)
        print(f"\nSaved metrics summary to: {out_path}")


if __name__ == "__main__":
    main()
