# AFAP Engine Input / Output Contracts (LOCKED)

These contracts define the canonical inputs and outputs for all engines.
Once locked, engines MUST conform to this structure.

---

## 1. Ratio Engine (CORE — Truth Layer)

**File:** engines/ratio_engine_core.py  
**Input:** financials_df (DataFrame)

**Output:** DataFrame

Required columns:
- Company
- Year
- current_ratio
- quick_ratio
- gross_margin
- operating_margin
- net_margin
- debt_equity
- interest_coverage
- asset_turnover
- roa
- roe

No flags. No severity. No explanations.

---

## 2. Trend Engine

**File:** engines/trend_engine.py  
**Input:** ratios_df (DataFrame)

**Output:** list[dict]

Keys:
- engine
- Company
- Year
- trends (dict)
- severity
- explanation

---

## 3. Cash Flow Health Engine

**File:** engines/cash_flow_engine.py  
**Input:** financials_df (DataFrame)

**Output:** list[dict]

Keys:
- engine
- Company
- Year
- metrics
- flags
- severity
- explanation

---

## 4. Anomaly & Efficiency Engine

**File:** engines/anomaly_efficiency_engine.py  
**Input:** ratios_df (DataFrame)

**Output:** list[dict]

Keys:
- engine
- Company
- Year
- metrics
- flags
- severity
- explanation

---

## 5. Solvency Engine

**File:** engines/solvency_engine.py  
**Input:** ratios_df (DataFrame)

**Output:** list[dict]

Keys:
- engine
- Company
- Year
- metrics
- flags
- severity
- explanation

---

## 6. Composite Risk Engine

**File:** engines/composite_risk_engine.py  
**Input:** outputs from engines 2–5

**Output:** DataFrame

Columns:
- Company
- Year
- composite_score
- risk_band

#Summary
| Engine               | Input           | Output Type  | Required Keys                    | Severity Output         |
| -------------------- | --------------- | ------------ | -------------------------------- | ----------------------- |
| Ratio Engine (CORE)  | `financials_df` | `DataFrame`  | Company, Year + 10 ratios        | ❌ none                  |
| Trend Engine         | `ratios_df`     | `list[dict]` | trends per ratio                 | up / down / flat        |
| Cash Flow Engine     | `financials_df` | `list[dict]` | operating_profit, coverage_proxy | stable / watch          |
| Anomaly & Efficiency | `ratios_df`     | `list[dict]` | anomaly_flags                    | normal / watch / high   |
| Solvency Engine      | `ratios_df`     | `list[dict]` | leverage_flags                   | stable / watch / action |
| Composite Risk       | all above       | `DataFrame`  | score, band                      | low / medium / high     |
