from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Tier

TIERS = [
    {"name": "free",   "display_name": "Free",
        "max_resume_uploads": 2,  "max_roasts_daily": 2},
    {"name": "google", "display_name": "Google",
        "max_resume_uploads": 5,  "max_roasts_daily": 10},
]


def seed_tiers(db: Session):
    for t in TIERS:
        result = db.execute(select(Tier).where(Tier.name == t["name"]))
        if not result.scalar_one_or_none():
            db.add(Tier(**t))
    db.commit()


def get_tier_by_name(name: str, db: Session) -> Tier | None:
    result = db.execute(select(Tier).where(Tier.name == name))
    return result.scalar_one_or_none()
