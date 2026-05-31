# Backend API

Flask REST API for authentication, loan application, KYC, and document management.

## Run

```bash
pip install -r requirements.txt
python -m app.app
```

## Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/loans/apply`
- `GET /api/v1/loans/{id}`
- `POST /api/v1/kyc/submit`
- `POST /api/v1/documents/upload`
