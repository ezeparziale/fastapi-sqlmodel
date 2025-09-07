from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.teams import Team, TeamRead


class HeroBase(SQLModel):
    name: str = Field(index=True, description="The name of the hero")
    secret_name: str = Field(description="The secret name of the hero")
    age: int | None = Field(default=None, index=True, description="The age of the hero")

    team_id: int | None = Field(
        default=None,
        foreign_key="team.id",
        description="The ID of the team the hero belongs to",
    )


class Hero(HeroBase, table=True):
    id: int | None = Field(
        default=None, primary_key=True, description="The unique ID of the hero"
    )

    team: Optional["Team"] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):
    id: int = Field(description="The unique ID of the hero")


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: str | None = Field(default=None, description="The name of the hero")
    secret_name: str | None = Field(
        default=None, description="The secret name of the hero"
    )
    age: int | None = Field(default=None, description="The age of the hero")
    team_id: int | None = Field(
        default=None, description="The ID of the team the hero belongs to"
    )


class HeroReadWithTeam(HeroRead):
    team: Optional["TeamRead"] = Field(
        default=None, description="The team the hero belongs to"
    )


from app.models.teams import Team, TeamRead

HeroReadWithTeam.model_rebuild()
