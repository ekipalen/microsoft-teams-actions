from enum import Enum
from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Dict, Optional


class Location(BaseModel):
    name: str = Field(description="Name of the location", default="")
    url: str = Field(description="URL of the location", default="")


class File(BaseModel):
    location: Location = Field(description="Location details")
    file: Dict = Field(description="File details", default={})


class FileList(BaseModel):
    files: list[File] = Field(description="List of files", default=[])


class ColumnType(str, Enum):
    text = "text"
    boolean = "boolean"
    datetime = "dateTime"
    number = "number"


class ListColumn(BaseModel):
    column_name: str = Field(description="Name of the column", default="")
    column_type: ColumnType = Field(description="Type of the column", default="")


class SharepointList(BaseModel):
    list_name: str = Field(description="Name of the list", default="")
    columns: list[ListColumn] = Field(description="List of columns", default=[])


class TeamDetails(BaseModel):
    display_name: str = Field(description="Display name of the team")
    description: str = Field(description="Description of the team")
    visibility: str = Field(
        description="Visibility of the team (public/private)", default="private"
    )


class UserSearch(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Email address of the user")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError(
                "At least one of email, first_name, or last_name must be provided"
            )
        return values
