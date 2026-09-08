# MLB Pythagorean Expectation

### Which teams won more or fewer games than their runs suggested?

**Python · pandas · matplotlib · MLB Stats API**

[Read the code](analyze.py) · [Inspect all 30 teams](data/mlb_pythagorean_2025.csv) · [Run it](#run-it) · [Back to profile](../../README.md)

![2025 MLB wins above and below Pythagorean expectation](charts/mlb_pythagorean_2025.png)

## The question

A team's record measures its result. Runs scored and allowed provide a different baseline. This project compares the two for all 30 MLB teams in the completed 2025 regular season.

The largest positive differences in the saved output were the Angels (+8.4 wins), Guardians (+7.8), and Marlins (+7.5). The largest negative differences were the White Sox (−10.0), Rangers (−9.9), and Rays (−7.6).

**A gap identifies a question to investigate; it does not identify its cause.** This analysis does not separate bullpen effects, close-game outcomes, roster timing, or randomness, and is not a forecasting model.

## Method and data

`analyze.py` retrieves American and National League regular-season standings from MLB's public Stats API at `https://statsapi.mlb.com/api/v1/standings`, with `leagueId=103,104`, `season=2025`, and `standingsTypes=regularSeason`.

```text
actual win percentage = wins / games played
expected win percentage = runs scored² / (runs scored² + runs allowed²)
expected wins = expected win percentage × games played
wins above expectation = actual wins − expected wins
```

The exponent is fixed at 2. Other formulations may produce different estimates. The saved CSV contains the original input totals and the derived fields rounded to four decimals. All 30 teams in this retained 2025 snapshot have 162 games, so ranking by percentage difference and wins difference produces the same order.

The chart was regenerated from the retained dataset for this publication; it is not a new live API pull.

## Run it

Use **Python 3.13**, the version tested with these pinned dependencies. Clone this public repository, then run from the project folder, preferably in an activated virtual environment:

```bash
git clone https://github.com/MichaelJNichols/MichaelJNichols.git
cd MichaelJNichols/projects/mlb-pythagorean-expectation
python -m pip install -r requirements.txt
python reproduce.py
python -m unittest -v test_analysis.py
```

After dependencies are installed, reproduction and tests work **without network access**. `reproduce.py` reads only the retained inputs, recalculates the results, and writes a CSV and PNG under `output/`, leaving the original dataset untouched.

For a fresh API retrieval:

```bash
python analyze.py --season 2025
```

The original live-fetch command writes to `data/` and `charts/` for the requested season and requires internet access. Current upstream totals can differ from a retained historical capture.

## Verification

Eight offline tests cover complete team records, the formula, every retained derived field, ordering and input preservation, invalid input rejection, mocked API mapping, HTTP-error propagation, and chart creation. Offline reproduction regenerated the saved CSV byte-for-byte during local and GitHub-hosted publication checks.

Direct dependencies are pinned in `requirements.txt`; local review used Python 3.13.5. This is not a fully locked transitive environment, and plot rasterization can vary between operating systems. [Publication review record](../../evidence/2026-09-08-publication-review.json).

## Contribution and publication

This is the existing completed analysis, now available to inspect and run. The original `analyze.py` and CSV are byte-identical to the reviewed project snapshot. An offline helper, input validation, and regression tests were added with AI assistance for the public release on September 8, 2026. The analytical method and findings were not changed.

Only this allowlisted example was copied into the public profile repository. The private lab's history and unrelated material remain private. No athlete, family, employer, or customer records are used. This is an independent project, not an MLB endorsement.
