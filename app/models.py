from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class RolePermission(SQLModel, table=True):
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: Optional[int] = Field(default=None, foreign_key="permission.id", primary_key=True)

class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    permissions: List[Permission] = Relationship(back_populates="roles", link_model=RolePermission)
    users: List["User"] = Relationship(back_populates="role")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="users")

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")