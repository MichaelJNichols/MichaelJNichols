# Improving MARCEL: 2021 OPS Projections

**R · tidyverse · Lahman · SABR Analytics Certification Level 3**

[Back to profile](../../README.md)

## The question

Can a hitter's walk rate, strikeout rate, and power help improve a simple OPS projection?

For my final project in SABR Analytics Certification Level 3, I reproduced the assignment's MARCEL baseline and built a linear model to correct its historical errors. After completing the course, I cleaned up the exploratory notebook work into a runnable R script in my private Baseball Analytics Lab.

## Results

| Evaluation | MARCEL MAE | Adjusted model MAE | Reduction |
| --- | ---: | ---: | ---: |
| Rolling backtest, 2010–2019 | 0.08435 | 0.08048 | 4.6% |
| Submitted 2021 evaluation | ~0.07818 | 0.06993 | ~10.6% |

MAE is mean absolute error in OPS; lower is better. The adjusted model beat the baseline in **8 of 10 historical backtest seasons**. The backtest averages give each season equal weight.

The 2021 figures are previously reported assignment evaluator results. The baseline MAE is inferred from the model's reported 0.06993 MAE plus the evaluator's 0.008248 MAE gap. The evaluator's separately reported median absolute error is a different metric.

## How it works

The assignment baseline weights three prior seasons' OPS 5/4/3, regresses toward .720 using plate appearances, and applies an age adjustment.

I combined multi-team batting stints into player-seasons using Lahman data. Historical examples require three consecutive prior seasons with at least 100 plate appearances each.

A linear regression predicts the baseline's error using age, recent OPS, OPS trend and volatility, reliability, walk rate, strikeout rate, and isolated power:

**Adjusted OPS = MARCEL OPS + predicted correction**

Each rolling backtest trains on years before the test season. The final model trains through 2019 and uses the assignment data plus 2020 batting components to project 2021. The submitted specification was locked before the 2021 evaluation.

## What the results do—and do not—show

The improvement is against the assignment's simplified MARCEL baseline, not every MARCEL implementation or a commercial projection system. The historical sample favors established hitters, and the shortened 2020 season makes recent batting rates less stable. The model does not explicitly adjust for parks, injuries, or changing league conditions.

The rolling backtest informed development; it is not an untouched evaluation of model selection. The separately reported 2021 evaluation covers one assignment sample.

My main takeaway: component batting information can improve a simple baseline while keeping the model understandable. Testing across seasons also makes the inconsistent years visible.

## Verification and project status

The cleaned script was run with R 4.6.1, tidyverse 2.0.0, and Lahman 14.0-0. It produced 175 complete player projections and reproduced the historical results above. The cleanup preserved both projection and backtest CSV values exactly.

The script reads the [public assignment data](https://huggingface.co/spaces/rkarthur/sabr3evaluation/raw/main/data/SABR3_data_for_assignment.csv) and uses historical batting data from the Lahman R package. It does not retrieve 2021 outcomes or rerun the external evaluator.

This page is a public project summary. The source code and generated submission remain in the private lab repository. Code cleanup and portfolio editing used AI assistance; the analytical specification and results were preserved.
