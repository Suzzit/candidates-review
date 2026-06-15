from datetime import datetime

import sqlalchemy as sa

from models import Base

class Users(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    fullname = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    role_applied = sa.Column(sa.String(255), nullable=False)

    status = sa.Column(sa.String(20), default="new", nullable=False)

    role = sa.Column(sa.String(20), default='reviewer', nullable=False)

    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
