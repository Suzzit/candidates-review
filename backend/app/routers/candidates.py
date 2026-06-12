import json
import math

from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy as sa

from app.models import engine
from app.routers.auth.jwt_utils import require_roles, get_current_user
from app.models.users import Users
from app.models.score import Score

router = APIRouter()

@router.get("/candidates")
def candidate_list(
    status: str | None = None,
    role_applied: str | None = None,
    skill: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 10,
    current_user: dict = Depends(require_roles("reviewer", "admin")),
):
    filters = []

    if status:
        filters.append(Users.status == status)

    if role_applied:
        filters.append(Users.role_applied.ilike(f"%{role_applied}%"))

    if skill:
        filters.append(Users.skills.like(f'%"{skill}"%'))

    if keyword:
        filters.append(
            sa.or_(
                Users.name.ilike(f"%{keyword}%"),
                Users.email.ilike(f"%{keyword}%"),
            )
        )

    base_query = sa.select(
        Users.id,
        Users.name,
        Users.email,
        Users.role_applied,
        Users.status,
        Users.skills,
        Users.created_at,
    ).where(
        *filters,
        Users.id != current_user.get('id')
    )

    count_query = sa.select(sa.func.count()).select_from(Users).where(*filters)

    offset = (page - 1) * page_size

    query = base_query.order_by(Users.id).limit(page_size).offset(offset)

    with engine.connect() as connection:
        total = connection.execute(count_query).scalar_one()
        rows = connection.execute(query).fetchall()

    items = []
    for row in rows:
        item = row._asdict()
        item["skills"] = json.loads(item["skills"] or "[]")
        items.append(item)

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if page_size else 0,
    }


@router.get("/candidates/{id}")
def candidate_detail(id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "candidate" and current_user["id"] != id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    query = sa.select(
        Users.id,
        Users.name,
        Users.email,
        Users.role_applied,
        Users.status,
        Users.skills,
        Users.internal_notes,
        Users.ai_summary,
        Users.created_at,
    ).where(Users.id == id)

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Candidate not found")

        candidate = result._asdict()
        candidate["skills"] = json.loads(candidate["skills"] or "[]")

        if current_user["role"] == "candidate":
            del candidate["internal_notes"]
            del candidate["ai_summary"]
            candidate["scores"] = []
            return candidate

        scores_query = sa.select(
            Score.id,
            Score.category,
            Score.score,
            Score.reviewer_id,
            Score.note,
            Score.created_at,
        ).where(
            Score.user_id == id
        )

        if current_user["role"] == "reviewer":
            del candidate["internal_notes"]
            scores_query = scores_query.where(Score.reviewer_id == current_user["id"])

        scores = connection.execute(scores_query).fetchall()

    candidate["scores"] = [row._asdict() for row in scores]

    return candidate