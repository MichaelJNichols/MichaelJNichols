"""Rebuild the published 2025 analysis without calling an external API."""
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
from analyze import PROJECT_DIR, calculate_expectation, save_chart

INPUT_COLUMNS = ["team", "division", "wins", "losses", "runs_scored", "runs_allowed"]


def load_snapshot(path: Path) -> pd.DataFrame:
    """Read and validate the complete 2025 MLB snapshot; ignore saved derived fields."""
    frame = pd.read_csv(path)
    missing = set(INPUT_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing input columns: {', '.join(sorted(missing))}")
    frame = frame[INPUT_COLUMNS].copy()
    if len(frame) != 30 or frame["team"].nunique() != 30:
        raise ValueError("The 2025 snapshot must contain 30 distinct teams.")
    if frame.isna().any().any():
        raise ValueError("Input fields cannot be missing.")
    for col in INPUT_COLUMNS[2:]:
        values = pd.to_numeric(frame[col], errors="raise")
        if ((values < 0) | (values % 1 != 0)).any():
            raise ValueError(f"{col} must contain finite nonnegative integers.")
        frame[col] = values.astype("int64")
    if not ((frame["wins"] + frame["losses"]) == 162).all():
        raise ValueError("This retained 2025 snapshot expects 162 games per team.")
    if ((frame["runs_scored"] + frame["runs_allowed"]) == 0).any():
        raise ValueError("Runs scored and allowed cannot both be zero.")
    return frame


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=PROJECT_DIR / "data/mlb_pythagorean_2025.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_DIR / "output")
    args = parser.parse_args()
    try:
        results = calculate_expectation(load_snapshot(args.input))
        args.output_dir.mkdir(parents=True, exist_ok=True)
        results.to_csv(args.output_dir / "mlb_pythagorean_2025.csv", index=False, float_format="%.4f")
        save_chart(results, 2025, args.output_dir / "mlb_pythagorean_2025.png")
    except (OSError, ValueError, pd.errors.ParserError) as error:
        parser.exit(1, f"Unable to reproduce analysis: {error}\n")
    print(results[["team", "wins", "expected_wins", "wins_above_expectation"]].to_string(index=False))
    print(f"\nReproduced 30-team analysis from retained input; saved to {args.output_dir}")


if __name__ == "__main__":
    main()
