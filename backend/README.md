# Backend API

Core backend service for the AI Microfinance Bank platform.

## Overview

This service handles:
- Loan application processing
- KYC (Know Your Customer) verification
- Document verification
- User management
- Integration with AI credit scoring engine

## Features

- RESTful API endpoints
- JWT authentication
- KYC workflows
- Document management
- API rate limiting

## Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

## API Endpoints

### Authentication
- POST /api/v1/auth/register - User registration
- POST /api/v1/auth/login - User login
- POST /api/v1/auth/refresh - Refresh token

### Loan Application
- POST /api/v1/loans/apply - Submit loan application
- GET /api/v1/loans/{loan_id} - Get loan details
- GET /api/v1/loans - List user loans

### KYC
- POST /api/v1/kyc/start - Start KYC process
- POST /api/v1/kyc/submit - Submit KYC details
- GET /api/v1/kyc/status - Get KYC status

### Documents
- POST /api/v1/documents/upload - Upload document
- GET /api/v1/documents/{doc_id} - Get document

## Environment Variables

Create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/microfinance
JWT_SECRET=your_secret_key
AI_ENGINE_URL=http://localhost:5001
PAYMENT_API_KEY=your_payment_api_key
```