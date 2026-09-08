# Baseball Analytics Lab — Pythagorean Expectation

### Which teams won more or fewer games than their runs suggested?

**Applied Python · Public API data · Reproducible analysis**  
**Completed project: 2025 MLB regular season · Write-up updated September 8, 2026**

[Back to profile](../README.md)

## The question

A team's win-loss record describes its result. Runs scored and allowed provide a different baseline for examining that result. This project compares the two for all 30 MLB teams in the completed 2025 regular season.

It is a focused analysis project, not a forecasting system or a claim of advanced predictive modeling.

## Method

The Python script retrieves American and National League regular-season standings from MLB's public Stats API and extracts team, division, wins, losses, runs scored, and runs allowed. It checks that the returned dataset contains 30 teams.

The implemented baseline uses an exponent of 2:

```text
actual winning percentage = wins / (wins + losses)

expected winning percentage =
    runs scored^2 / (runs scored^2 + runs allowed^2)

expected wins = expected winning percentage × games played

wins above expectation = actual wins − expected wins
```

The project uses `requests` for retrieval, pandas for tabular calculations and export, and matplotlib for a horizontal comparison chart. The script accepts a season argument and produces a season-specific CSV and chart.

## Selected results from the retained output

| Team | Actual wins | Expected wins | Difference |
|---|---:|---:|---:|
| Los Angeles Angels | 72 | 63.6 | +8.4 |
| Cleveland Guardians | 88 | 80.2 | +7.8 |
| Miami Marlins | 79 | 71.5 | +7.5 |
| Tampa Bay Rays | 77 | 84.6 | −7.6 |
| Texas Rangers | 81 | 90.9 | −9.9 |
| Chicago White Sox | 60 | 70.0 | −10.0 |

Values are rounded to one decimal and summarize the largest positive and negative differences in the project's saved 30-team dataset. The figures above come from that retained output, not a new live data pull performed for this write-up.

## Interpretation

The calculation identifies a gap worth investigating. It does not identify the cause of that gap or establish that a team was inherently better, worse, luckier, or better managed than its record suggests.

The analysis uses one simple baseline. It does not evaluate alternative exponents, estimate uncertainty, separate close-game and bullpen effects, or test out-of-sample predictions. Those are possible follow-on questions, not completed parts of this project.

The useful distinction is between **measuring a difference** and **explaining why it happened**.

## What the project demonstrates

Taking a defined baseball question through API retrieval, a structured dataset, explicit calculations, ranked output, a chart, and a written interpretation. It also demonstrates making the method inspectable and documenting the limits instead of turning a descriptive result into an unsupported causal claim.

This work builds hands-on Python depth alongside my product and operations projects. SQL and R remain separate learning/project directions; they are not represented here as completed analyses.

## Evidence and availability

This public summary was checked against the implemented Python script, project README, and saved CSV. The source repository, executable script, full CSV, and chart remain private; this page is the public analytical write-up, not an open-source release. No private athlete, customer, or employer data is used.
