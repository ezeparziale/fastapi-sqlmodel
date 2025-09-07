from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.database import get_session
from app.models import Hero, HeroCreate, HeroRead, HeroReadWithTeam, HeroUpdate

router = APIRouter()


@router.post("/")
def create_hero(
    *, session: Session = Depends(get_session), hero: HeroCreate
) -> HeroRead:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/")
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> List[HeroRead]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/{hero_id}")
def read_hero(
    *, session: Session = Depends(get_session), hero_id: int
) -> HeroReadWithTeam:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/{hero_id}")
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
) -> HeroRead:
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.delete("/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int) -> Any:

    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
