# Payment Processor

Flask service for payment initiation, disbursement, EMI scheduling, and webhook updates.

## Run

```bash
pip install -r requirements.txt
python -m app.app
```

## Endpoints

- `POST /api/v1/payments/initiate`
- `POST /api/v1/disbursement/initiate`
- `GET /api/v1/payments/{id}`
- `POST /api/v1/emi/schedule`
- `POST /api/v1/payments/webhook`
