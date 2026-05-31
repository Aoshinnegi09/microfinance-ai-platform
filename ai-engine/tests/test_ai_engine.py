from app.app import create_app


def test_score_and_approval_endpoints():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    payload = {
        "features": {
            "monthly_income": 50000,
            "monthly_expense": 20000,
            "existing_debt": 10000,
            "repayment_history": 0.9,
            "requested_amount": 50000,
            "group": "group_b",
        }
    }

    score = client.post("/api/v1/score", json=payload)
    assert score.status_code == 200
    assert 300 <= score.get_json()["credit_score"] <= 850

    approval = client.post("/api/v1/predict-approval", json=payload)
    assert approval.status_code == 200
    assert "fair_lending" in approval.get_json()


def test_interest_and_loan_amount():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    ir = client.post("/api/v1/calculate-interest-rate", json={"credit_score": 720, "loan_amount": 60000})
    assert ir.status_code == 200

    amt = client.post(
        "/api/v1/calculate-loan-amount",
        json={"monthly_income": 45000, "monthly_expense": 15000, "existing_emi": 5000},
    )
    assert amt.status_code == 200
    assert amt.get_json()["recommended_loan_amount"] > 0
