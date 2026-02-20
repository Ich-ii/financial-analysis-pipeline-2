# contracts/engine_interfaces.py

from typing import List, Dict, TypedDict, Optional


# ---------------------------
# Base Record (ALL engines)
# ---------------------------

class BaseEngineRecord(TypedDict):
    Company: str
    Year: int


# ---------------------------
# Ratio Engine
# ---------------------------

class RatioRecord(BaseEngineRecord):
    current_ratio: Optional[float]
    quick_ratio: Optional[float]
    debt_to_equity: Optional[float]
    gross_margin: Optional[float]
    operating_margin: Optional[float]
    net_margin: Optional[float]
    roa: Optional[float]
    roe: Optional[float]


# ---------------------------
# Trend Engine
# ---------------------------

class TrendRecord(BaseEngineRecord):
    metric: str
    trend: str            # "up", "down", "flat", "volatile"
    slope: float
    strength: float       # 0–1
    flag: Optional[str]   # "deteriorating", "improving", None


# ---------------------------
# Cash Flow Health Engine
# ---------------------------

class CashFlowRecord(BaseEngineRecord):
    operating_cf: float
    investing_cf: float
    financing_cf: float
    cf_pattern: str       # "healthy", "strained", "burning"
    cf_risk_flag: Optional[str]


# ---------------------------
# Anomaly & Efficiency Engine
# ---------------------------

class AnomalyRecord(BaseEngineRecord):
    metric: str
    anomaly_type: str     # "spike", "drop", "outlier"
    severity: str         # "low", "medium", "high"
    z_score: float
    explanation_code: str


# ---------------------------
# Solvency Engine
# ---------------------------

class SolvencyRecord(BaseEngineRecord):
    debt_to_equity: Optional[float]
    interest_coverage: Optional[float]
    solvency_risk: str    # "low", "moderate", "high"
    breach_flag: bool


# ---------------------------
# Composite Risk Output
# ---------------------------

class CompositeRiskRecord(BaseEngineRecord):
    liquidity_score: float
    solvency_score: float
    efficiency_score: float
    overall_risk_score: float   # 0–100
    risk_band: str              # "low", "medium", "high"
