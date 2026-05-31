from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    kyc_status = db.Column(db.String(50), default="pending", nullable=False)


class Loan(db.Model, TimestampMixin):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default="under_review", nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    approval_date = db.Column(db.DateTime)
    disbursement_date = db.Column(db.DateTime)


class Application(db.Model, TimestampMixin):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default="submitted", nullable=False)
    credit_score = db.Column(db.Float, nullable=False)


class Payment(db.Model, TimestampMixin):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey("loans.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)
    payment_date = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(120), unique=True)


class Document(db.Model, TimestampMixin):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doc_type = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(255), nullable=False)


class KYCRecord(db.Model, TimestampMixin):
    __tablename__ = "kyc_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    gov_id = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)
