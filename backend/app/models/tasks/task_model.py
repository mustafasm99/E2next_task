from app.models.base_model import DbBaseModel
from sqlmodel import Column, Integer, String, Boolean, ForeignKey, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users.user import User


class Task(DbBaseModel, table=True):
    __tablename__ = "tasks"
    id: int = Field(
        sa_column=Column(Integer, primary_key=True, autoincrement=True),
    )
    title: str = Field(sa_column=Column(String, nullable=False))
    description: str = Field(sa_column=Column(String, nullable=True))
    completed: bool = Field(default=False, sa_column=Column(Boolean, default=False))
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("users.id"), nullable=False),
    )

    user: "User" = Relationship(back_populates="tasks")
