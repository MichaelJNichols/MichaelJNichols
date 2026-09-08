"""Compare MLB teams' actual records with Pythagorean expectation."""

from argparse import ArgumentParser
import os
from pathlib import Path

import pandas as pd
import requests


API_URL = "https://statsapi.mlb.com/api/v1/standings"
DEFAULT_SEASON = 2025
PROJECT_DIR = Path(__file__).resolve().parent

# Keep Matplotlib's generated cache inside this self-contained project.
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_DIR / ".matplotlib"))
import matplotlib.pyplot as plt  # noqa: E402  (configured after MPLCONFIGDIR)


def fetch_standings(season: int) -> pd.DataFrame:
    """Download regular-season standings for all American and National League teams."""
    params = {
        "leagueId": "103,104",  # American League and National League
        "season": season,
        "standingsTypes": "regularSeason",
        "hydrate": "team(division)",
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    rows = []
    for division in response.json()["records"]:
        for record in division["teamRecords"]:
            rows.append(
                {
                    "team": record["team"]["name"],
                    "division": record["team"]["division"]["name"],
                    "wins": record["wins"],
                    "losses": record["losses"],
                    "runs_scored": record["runsScored"],
                    "runs_allowed": record["runsAllowed"],
                }
            )

    standings = pd.DataFrame(rows)
    if len(standings) != 30:
        raise ValueError(f"Expected 30 MLB teams, but the API returned {len(standings)}.")
    return standings


def calculate_expectation(standings: pd.DataFrame) -> pd.DataFrame:
    """Add actual, expected, and difference columns to the standings."""
    results = standings.copy()
    games = results["wins"] + results["losses"]
    results["actual_win_pct"] = results["wins"] / games

    # Bill James's classic Pythagorean formula uses an exponent of 2.
    runs_squared = results["runs_scored"] ** 2
    results["expected_win_pct"] = runs_squared / (
        runs_squared + results["runs_allowed"] ** 2
    )
    results["difference"] = results["actual_win_pct"] - results["expected_win_pct"]
    results["expected_wins"] = results["expected_win_pct"] * games
    results["wins_above_expectation"] = results["wins"] - results["expected_wins"]

    return results.sort_values("difference", ascending=False).reset_index(drop=True)


def save_chart(results: pd.DataFrame, season: int, output_path: Path) -> None:
    """Create a horizontal chart of wins above or below expectation."""
    chart_data = results.sort_values("wins_above_expectation")
    colors = ["#c44e52" if value < 0 else "#4c72b0" for value in chart_data["wins_above_expectation"]]

    fig, ax = plt.subplots(figsize=(11, 10))
    ax.barh(chart_data["team"], chart_data["wins_above_expectation"], color=colors)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_title(f"{season} MLB Wins Above/Below Pythagorean Expectation")
    ax.set_xlabel("Actual wins minus expected wins")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--season", type=int, default=DEFAULT_SEASON)
    args = parser.parse_args()

    data_dir = PROJECT_DIR / "data"
    chart_dir = PROJECT_DIR / "charts"
    data_dir.mkdir(exist_ok=True)
    chart_dir.mkdir(exist_ok=True)

    results = calculate_expectation(fetch_standings(args.season))
    csv_path = data_dir / f"mlb_pythagorean_{args.season}.csv"
    chart_path = chart_dir / f"mlb_pythagorean_{args.season}.png"
    results.to_csv(csv_path, index=False, float_format="%.4f")
    save_chart(results, args.season, chart_path)

    display_columns = ["team", "wins", "losses", "actual_win_pct", "expected_win_pct", "wins_above_expectation"]
    print(results[display_columns].to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    print(f"\nSaved {csv_path.relative_to(PROJECT_DIR)}")
    print(f"Saved {chart_path.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
