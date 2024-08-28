from uuid import UUID
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from fastapi_pagination import Page

class ExpenseBase(BaseModel):
    """
    Schema representing the base fields for creating and updating an expense.
    """
    category_id: UUID
    subject: str = Field(..., min_length=2, max_length=100)
    expense_date: date
    amount: float = Field(..., gt=0)
    reimbursable: bool = Field(default=False)
    description: Optional[str] = Field(default=None, max_length=500)
    invoice_image: Optional[bytes] = None
    employee: Optional[str] = Field(default=None, max_length=100)


class ExpenseCreate(ExpenseBase):
    """
    Schema representing the fields required to create a new expense.
    Inherits: ExpenseBase: Base schema with common expense fields.
    """

class ExpenseUpdate(BaseModel):
    """
    Schema representing the fields required to update an expense.
    All fields are optional to allow partial updates.
    """
    category_id: Optional[UUID]
    subject: Optional[str] = Field(None, min_length=2, max_length=100)
    expense_date: Optional[date]
    amount: Optional[float] = Field(None, gt=0)
    reimbursable: Optional[bool]
    description: Optional[str] = Field(None, max_length=500)
    invoice_image: Optional[bytes] = None
    employee: Optional[str] = Field(None, max_length=100)

class Expense(ExpenseBase):
    """
    Schema representing an expense with a unique identifier.
    """
    expenses_id: UUID
    user_id: UUID
    updated_at: datetime

    class Config:
        """Configuration for the Pydantic model."""
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }

PagedExpense = Page[Expense]
