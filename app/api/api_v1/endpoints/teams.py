from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.database import get_session
from app.models import Team, TeamCreate, TeamRead, TeamReadWithHeroes, TeamUpdate

router = APIRouter()


@router.post("/")
def create_team(
    *, session: Session = Depends(get_session), team: TeamCreate
) -> TeamRead:
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/")
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> List[TeamRead]:
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/{team_id}")
def read_team(
    *, team_id: int, session: Session = Depends(get_session)
) -> TeamReadWithHeroes:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}")
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
) -> TeamRead:
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int) -> Any:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
