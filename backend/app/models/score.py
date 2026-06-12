from datetime import datetime

import sqlalchemy as sa

from app.models import Base


class Score(Base):
    __tablename__ = "scores"

    id = sa.Column(sa.Integer, primary_key=True, index=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)

    category = sa.Column(sa.String(100), nullable=False)

    # 1-5
    score = sa.Column(sa.Integer, nullable=False)

    reviewer_id = sa.Column(sa.Integer, nullable=False)

    note = sa.Column(sa.Text, nullable=True)

    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    user = sa.orm.relationship("Users", back_populates="scores")