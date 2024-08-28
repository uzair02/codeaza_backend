"""
This module defines Pydantic schemas for user-related data.

These schemas are used for validating and serializing user data, such as
user creation, login, and profile information, within the FastAPI application.

Imports:
    - BaseModel from Pydantic for creating data validation and serialization models.
    - EmailStr from Pydantic for validating email addresses.
    - UUID4 from Pydantic for handling UUID fields.
    - Optional from typing for defining optional fields.
"""

from pydantic import BaseModel, UUID4


class UserBase(BaseModel):
    """
    Base schema for user data, used as a base class for other user schemas.

    Attributes:
        username (str): The username of the user.

    """

    username: str


class UserCreate(UserBase):
    """
    Schema for user creation, extending the base user schema.

    Attributes:
        password (str): The password for the user account.
    """

    password: str


class User(UserBase):
    """
    Schema for a user profile, extending the base user schema.

    Attributes:
        id (UUID4): The unique identifier for the user.
        is_active (bool): Indicates whether the user account is active.
    """

    user_id: UUID4
    is_active: bool

    class Config:
        """
        Configuration for the Pydantic model.

        Enables compatibility with ORM models by allowing the model to
        be populated from attributes of an ORM model instance.
        """

        from_attributes = True
