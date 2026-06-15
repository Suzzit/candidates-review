from datetime import datetime

import sqlalchemy as sa

from app.models import Base


class Score(Base):
    __tablename__ = "scores"

    id = sa.Column(sa.Integer, primary_key=True, index=True)

    category = sa.Column(sa.String(100), nullable=False)
    score = sa.Column(sa.Integer, nullable=False)
    note = sa.Column(sa.Text, nullable=True)

    reviewer_id = sa.Column(sa.Integer, nullable=False, unique=True)
    candidate_id = sa.Column(sa.Integer, nullable=False, unique=True)

    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
