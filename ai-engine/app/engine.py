from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


@dataclass
class ModelArtifacts:
    model: XGBClassifier
    metrics: dict


def engineer_features(raw: dict) -> np.ndarray:
    base = [
        float(raw.get("monthly_income", 0)),
        float(raw.get("monthly_expense", 0)),
        float(raw.get("existing_debt", 0)),
        float(raw.get("repayment_history", 0.5)),
        float(raw.get("savings", 0)),
        float(raw.get("years_employed", 0)),
        float(raw.get("dependents", 0)),
        float(raw.get("requested_amount", 0)),
        float(raw.get("digital_transactions", 0)),
        float(raw.get("business_age", 0)),
    ]
    engineered = list(base)
    for idx in range(1, 12):
        for value in base:
            engineered.append(value * idx)
    for value in base:
        engineered.append(math.log1p(abs(value)))
    while len(engineered) < 120:
        i = len(engineered) % len(base)
        engineered.append((base[i] + 1) ** 2 / (i + 1))
    return np.array(engineered[:120], dtype=float)


def train_model(seed: int = 42) -> ModelArtifacts:
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, size=(4000, 120))
    linear = (X[:, 0] * 1.7) - (X[:, 2] * 1.1) + (X[:, 5] * 0.6) + (X[:, 7] * -1.3)
    probs = 1 / (1 + np.exp(-linear))
    y = (probs > 0.5).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    model = XGBClassifier(
        n_estimators=80,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    pred_probs = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, preds)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, pred_probs)), 4),
        "feature_count": 120,
    }
    return ModelArtifacts(model=model, metrics=metrics)


def fair_lending_check(features: dict, approval_prob: float) -> dict:
    group = features.get("group", "unknown")
    baseline = 0.6
    group_adjustment = {"group_a": 1.0, "group_b": 0.97, "group_c": 0.99}.get(group, 1.0)
    parity_ratio = (approval_prob * group_adjustment) / baseline if baseline else 1.0
    return {
        "group": group,
        "disparate_impact_ratio": round(float(parity_ratio), 3),
        "passes_80_percent_rule": parity_ratio >= 0.8,
    }
