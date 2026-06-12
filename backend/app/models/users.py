import enum
import json
from datetime import datetime

import sqlalchemy as sa

from app.models import Base
from app.models.score import Score


class UserStatus(enum.Enum):
    NEW = 'new'
    REVIEWED = 'reviewed'
    HIRED = 'hired'
    REJECTED = 'rejected'

class Users(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    role_applied = sa.Column(sa.String(255), nullable=False)

    status = sa.Column(sa.String(20), default="new", nullable=False)

    # candidate, reviewer, admin
    role = sa.Column(sa.String(50), default="reviewer", nullable=False)

    # SQLite doesn't support arrays natively,
    # so store skills as JSON text.
    skills = sa.Column(sa.Text, default="[]")

    internal_notes = sa.Column(sa.Text, nullable=True)

    ai_summary = sa.Column(sa.Text, nullable=True)

    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    scores = sa.orm.relationship(
        Score, back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def skills_list(self):
        return json.loads(self.skills)

    @skills_list.setter
    def skills_list(self, value):
        self.skills = json.dumps(value)