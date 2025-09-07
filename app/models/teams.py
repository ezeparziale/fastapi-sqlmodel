from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.heros import Hero, HeroRead


class TeamBase(SQLModel):
    name: str = Field(index=True, description="The name of the team")
    headquarters: str = Field(description="The headquarters of the team")


class Team(TeamBase, table=True):
    id: int | None = Field(
        default=None, primary_key=True, description="The unique identifier of the team"
    )

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int = Field(description="The unique identifier of the team")


class TeamUpdate(SQLModel):
    id: int | None = Field(
        default=None, description="The unique identifier of the team"
    )
    name: str | None = Field(default=None, description="The name of the team")
    headquarters: str | None = Field(
        default=None, description="The headquarters of the team"
    )


class TeamReadWithHeroes(TeamRead):
    heroes: List["HeroRead"] = Field(
        default_factory=list, description="List of heroes in the team"
    )


from app.models.heros import Hero, HeroRead

TeamReadWithHeroes.model_rebuild()
