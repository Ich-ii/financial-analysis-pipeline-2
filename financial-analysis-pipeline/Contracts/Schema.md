# Financial Analysis Engine Interfaces

This document defines the locked input/output contracts for all engines.
All engines MUST conform to these structures.

---

## Common Fields
| Field   | Type | Description |
|-------|------|-------------|
| Company | str | Legal entity name |
| Year | int | Financial period |

---

## Ratio Engine
Outputs per Company-Year:
- current_ratio
- quick_ratio
- debt_to_equity
- gross_margin
- operating_margin
- net_margin
- roa
- roe

Missing values allowed (None).

---

## Trend Engine
Outputs per Company-Year per metric:
- metric
- trend (up/down/flat/volatile)
- slope
- strength (0–1)
- flag (optional)

---

## Cash Flow Health Engine
- operating_cf
- investing_cf
- financing_cf
- cf_pattern
- cf_risk_flag

---

## Anomaly & Efficiency Engine
One record per detected anomaly:
- metric
- anomaly_type
- severity
- z_score
- explanation_code

---

## Solvency Engine
- debt_to_equity
- interest_coverage
- solvency_risk
- breach_flag

---

## Composite Risk Scoring
- liquidity_score (0–1)
- solvency_score (0–1)
- efficiency_score (0–1)
- overall_risk_score (0–100)
- risk_band

