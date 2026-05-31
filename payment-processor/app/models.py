from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default="initiated", nullable=False)
    payment_date = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(120), unique=True, nullable=False)
    provider = db.Column(db.String(50), default="mock_upi", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Disbursement(db.Model):
    __tablename__ = "disbursements"

    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default="processing", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
