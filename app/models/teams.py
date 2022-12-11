from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    headquarters: Optional[str] = None


class TeamReadWithHeroes(TeamRead):
    heroes: List["HeroRead"] = []


from app.models.heros import Hero, HeroRead

Team.update_forward_refs()
TeamReadWithHeroes.update_forward_refs()
