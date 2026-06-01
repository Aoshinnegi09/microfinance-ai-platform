import io
import os

import pytest
from sqlalchemy.exc import OperationalError

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["AI_ENGINE_URL"] = "http://localhost:5999"

from app.app import _init_db_with_retry, create_app  # noqa: E402
from app.models import db  # noqa: E402


@pytest.fixture
def client(monkeypatch):
    app = create_app()
    app.config.update(TESTING=True)

    def fake_post(url, json, timeout):
        class Resp:
            ok = True

            def raise_for_status(self):
                return None

            def json(self):
                if url.endswith("/score"):
                    return {"credit_score": 720}
                return {"interest_rate": 14.5}

        return Resp()

    monkeypatch.setattr("app.routes.requests.post", fake_post)

    with app.app_context():
        db.create_all()

    with app.test_client() as c:
        yield c


def _register(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "a@example.com", "phone": "9999999999", "password": "pass123", "name": "Alice"},
    )
    return resp.get_json()["token"]


def test_auth_and_loan_flow(client):
    token = _register(client)
    headers = {"Authorization": "Bearer " + token}

    loan_resp = client.post(
        "/api/v1/loans/apply",
        headers=headers,
        json={"loan_amount": 10000, "purpose": "shop", "features": {"income": 50000}},
    )
    assert loan_resp.status_code == 201
    loan_id = loan_resp.get_json()["loan_id"]

    get_resp = client.get(f"/api/v1/loans/{loan_id}", headers=headers)
    assert get_resp.status_code == 200


def test_kyc_and_document_upload(client):
    token = _register(client)
    headers = {"Authorization": "Bearer " + token}

    kyc = client.post("/api/v1/kyc/submit", headers=headers, json={"gov_id": "A12345678", "address": "Main Street"})
    assert kyc.status_code == 200
    assert kyc.get_json()["status"] == "approved"

    data = {"doc_type": "id_card", "file": (io.BytesIO(b"x"), "id.png")}
    doc = client.post("/api/v1/documents/upload", headers=headers, content_type="multipart/form-data", data=data)
    assert doc.status_code == 201


def test_db_init_retries_on_temporary_operational_error(monkeypatch):
    app = create_app()
    calls = {"count": 0}

    def flaky_create_all():
        calls["count"] += 1
        if calls["count"] == 1:
            raise OperationalError(statement="SELECT 1", params=None, orig=Exception("temporary failure"))

    monkeypatch.setattr("app.app.db.create_all", flaky_create_all)
    monkeypatch.setattr("app.app.time.sleep", lambda *_: None)

    _init_db_with_retry(app, retries=2, delay_seconds=0)
    assert calls["count"] == 2
