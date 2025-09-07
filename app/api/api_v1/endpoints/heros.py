from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.database import get_db
from app.models import Hero, HeroCreate, HeroRead, HeroReadWithTeam, HeroUpdate

router = APIRouter()


@router.post("/")
def create_hero(*, db: Session = Depends(get_db), hero: HeroCreate) -> HeroRead:
    db_hero = Hero.model_validate(hero)
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero


@router.get("/")
def read_heroes(
    *,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> List[HeroRead]:
    heroes = db.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/{hero_id}")
def read_hero(*, db: Session = Depends(get_db), hero_id: int) -> HeroReadWithTeam:
    hero = db.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/{hero_id}")
def update_hero(
    *, db: Session = Depends(get_db), hero_id: int, hero: HeroUpdate
) -> HeroRead:
    db_hero = db.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero


@router.delete("/{hero_id}")
def delete_hero(*, db: Session = Depends(get_db), hero_id: int) -> Any:

    hero = db.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    db.delete(hero)
    db.commit()
    return {"ok": True}
