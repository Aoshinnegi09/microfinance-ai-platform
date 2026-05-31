import os

os.environ["PAYMENT_DATABASE_URL"] = "sqlite:///:memory:"

from app.app import create_app  # noqa: E402


def test_payment_lifecycle():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    init = client.post("/api/v1/payments/initiate", json={"loan_id": 1, "amount": 999.5})
    assert init.status_code == 201
    payload = init.get_json()

    get_resp = client.get(f"/api/v1/payments/{payload['payment_id']}")
    assert get_resp.status_code == 200

    hook = client.post("/api/v1/payments/webhook", json={"transaction_id": payload["transaction_id"], "status": "completed"})
    assert hook.status_code == 200


def test_emi_schedule():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    resp = client.post("/api/v1/emi/schedule", json={"principal": 12000, "annual_interest_rate": 12, "tenure_months": 12})
    assert resp.status_code == 200
    assert len(resp.get_json()["schedule"]) == 12
