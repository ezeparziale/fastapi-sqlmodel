from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.heros import Hero, HeroRead


class TeamBase(SQLModel):
    name: str = Field(
        index=True,
        description="The name of the team",
        schema_extra={"examples": ["Justice League"]},
    )
    headquarters: str = Field(
        description="The headquarters of the team",
        schema_extra={"examples": ["Hall of Justice"]},
    )


class Team(TeamBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        description="The unique identifier of the team",
        schema_extra={"examples": [1]},
    )

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int = Field(
        description="The unique identifier of the team", schema_extra={"examples": [1]}
    )


class TeamUpdate(SQLModel):
    id: int | None = Field(
        default=None,
        description="The unique identifier of the team",
        schema_extra={"examples": [1]},
    )
    name: str | None = Field(
        default=None,
        description="The name of the team",
        schema_extra={"examples": ["Justice League"]},
    )
    headquarters: str | None = Field(
        default=None,
        description="The headquarters of the team",
        schema_extra={"examples": ["Hall of Justice"]},
    )


class TeamReadWithHeroes(TeamRead):
    heroes: List["HeroRead"] = Field(
        default_factory=list, description="List of heroes in the team"
    )


from app.models.heros import Hero, HeroRead

TeamReadWithHeroes.model_rebuild()
