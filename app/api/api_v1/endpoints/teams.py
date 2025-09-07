from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.db.database import get_db
from app.models import Team, TeamCreate, TeamRead, TeamReadWithHeroes, TeamUpdate

router = APIRouter()


@router.post("/")
def create_team(*, db: Session = Depends(get_db), team: TeamCreate) -> TeamRead:
    """Create a new team"""
    db_team = Team.model_validate(team)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/")
def read_teams(
    *,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> List[TeamRead]:
    """Retrieve teams"""
    teams = db.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/{team_id}")
def read_team(*, team_id: int, db: Session = Depends(get_db)) -> TeamReadWithHeroes:
    """Get team by ID"""
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}")
def update_team(
    *,
    db: Session = Depends(get_db),
    team_id: int,
    team: TeamUpdate,
) -> TeamRead:
    """Update a team"""
    db_team = db.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.delete("/{team_id}")
def delete_team(*, db: Session = Depends(get_db), team_id: int) -> None:
    """Delete a team"""
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
