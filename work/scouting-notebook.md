# Scouting Notebook

### Better evidence without outsourcing the evaluation.

**Baseball decision support · Multi-source data · Product operations**  
**Updated September 8, 2026**

[Open the public demo](https://roguebaseballiq.com/scouting-demo/) · [Rogue Baseball Intelligence](https://roguebaseballiq.com/) · [Back to profile](../README.md)

## The problem

A player page can supply plenty of statistics without helping an evaluator make a better report. Observation, interpretation, projection, uncertainty, and subsequent evidence can easily collapse into one confident-sounding conclusion.

I built the Scouting Notebook around a different sequence: make the observation explicit, state the judgment and its confidence, then check it against appropriate data.

**Observe → Interpret → Grade → Project → Confidence → Data Check → Reconcile → Next Look → Retrospective**

The governing principle is **scout first; data second**. Imported statistics should support or challenge a judgment, not generate a scouting grade.

## What exists

A working public demonstration includes published report snapshots and an interactive player-data pipeline. The private founder workspace supports player identity, live/video/hybrid evaluation context, position-player and pitcher report structures, projections, confidence, evidence, and next-look objectives.

The public reports retain their evaluation-date context. The separate live pipeline resolves current player assignment and source coverage. That distinction prevents a later statistical update from being mistaken for information the evaluator had at the original look.

The full evaluator-calibration vision is broader than the current MVP. A public report snapshot does not establish that every planned locking, reconciliation, or retrospective workflow is complete.

## Data decisions that matter

| Decision | Why it matters |
|---|---|
| Use MLBAM as the primary identity key | Reduces the risk of combining records for the wrong player. |
| Keep hitter and pitcher schemas separate | Pitching opponent averages are not a pitcher's batting line. |
| Respect competition level | MLB tracking coverage and minor-league official statistics cannot be treated as interchangeable. |
| Retain source, definition, availability, and capture context | Differences across sources are information to explain, not numbers to silently overwrite. |
| Treat untracked values as missing, not zero | Avoids distorting applicable denominators and apparent performance. |

The data work uses MLB Stats API for identity and official context, Baseball Savant/Statcast for tracking where available, and Baseball-Reference and FanGraphs for independent performance/value context. Not every source covers every player, level, metric, or window.

## Operating the pipeline

The implementation progressed beyond a one-time data pull. Work included sharding large static datasets, scheduled refreshes, record and coverage validation, protection against competing publication writes, transient retries, and incident escalation.

The bounded-recovery change preserves the last validated committed data when a refresh fails. Automated recovery reruns defined workflows; it does not autonomously rewrite application logic, schemas, credentials, or permissions.

These controls are implemented operating mechanisms, not a claim of continuous uptime or permanently fresh upstream data. External sources can still fail or change.

## My contribution

I defined the evaluator workflow, report structure, source rules, product priorities, and acceptance expectations, and directed AI-assisted implementation and iteration. Scouting practice and report preparation shaped the product rather than being added as decoration around a statistics dashboard.

## What this demonstrates

For baseball work, the project connects observation and data while keeping level, role, uncertainty, and the next evaluation question visible. For broader product and operations work, it demonstrates data-contract design, external-dependency management, exception handling, and the discipline to explain what a result does and does not establish.

## Scope and evidence

The public demo is directly inspectable. Implementation and operating details in this summary were reviewed against the private product handoff and merged reliability work; private source and raw evaluator drafts are not published here. This is an independent project, not an MLB, club, or data-provider endorsement.
