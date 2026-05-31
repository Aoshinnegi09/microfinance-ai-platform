# AI-Powered Microfinance Bank Platform

Production-oriented multi-service platform implementing:

- **Backend API** (Flask + JWT + SQLAlchemy)
- **AI Credit Scoring Engine** (Flask + XGBoost + 120 engineered features)
- **Payment Processor** (Flask EMI/disbursement/payment workflows)
- **Mobile Web App** (React + responsive dashboards/forms)
- **Docker Compose** local deployment with PostgreSQL

## Services

| Service | Port | Key Endpoints |
|---|---:|---|
| backend | 5000 | `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/loans/apply`, `/api/v1/loans/{id}`, `/api/v1/kyc/submit`, `/api/v1/documents/upload` |
| ai-engine | 5001 | `/api/v1/score`, `/api/v1/predict-approval`, `/api/v1/calculate-interest-rate`, `/api/v1/calculate-loan-amount` |
| payment-processor | 5002 | `/api/v1/payments/initiate`, `/api/v1/disbursement/initiate`, `/api/v1/payments/{id}`, `/api/v1/emi/schedule` |
| mobile-app | 5173 | Responsive UI for auth, loans, KYC, docs, status, repayment |

## Quick Start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

Open `http://localhost:5173` for the UI.

## Local Development (without Docker)

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.app
```

### AI Engine
```bash
cd ai-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.app
```

### Payment Processor
```bash
cd payment-processor
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.app
```

### Mobile App
```bash
cd mobile-app
npm install
npm run dev
```

## Database Schema

`db-init/01_schema.sql` initializes:
- users
- loans
- applications
- payments
- documents
- kyc_records

## Testing

```bash
cd backend && pytest
cd ai-engine && pytest
cd payment-processor && pytest
cd mobile-app && npm run build
```
