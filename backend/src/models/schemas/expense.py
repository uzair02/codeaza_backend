from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

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
    invoice_image: Optional[str]
    description: Optional[str] = Field(default=None, max_length=500)
    employee: Optional[str] = Field(default=None, max_length=100)

class ExpenseCreate(BaseModel):
    """
    Schema representing the fields required to create a new expense.
    Inherits: ExpenseBase: Base schema with common expense fields.
    """
    category_id: UUID
    subject: str = Field(..., min_length=2, max_length=100)
    expense_date: date
    amount: float = Field(..., gt=0)
    reimbursable: bool = Field(default=False)
    description: Optional[str] = Field(default=None, max_length=500)
    employee: Optional[str] = Field(default=None, max_length=100)

class ExpenseUpdate(BaseModel):
    """
    Schema representing the fields required to update an expense.
    All fields are optional to allow partial updates.
    """
    category_id: Optional[UUID] = None
    subject: Optional[str] = Field(None, min_length=2, max_length=100)
    expense_date: Optional[date] = None
    amount: Optional[float] = Field(None, gt=0)
    reimbursable: Optional[bool] = None
    description: Optional[str] = Field(None, max_length=500)
    employee: Optional[str] = Field(None, max_length=100)

class Expense(ExpenseBase):
    """
    Schema representing an expense with a unique identifier.
    """
    expenses_id: UUID
    user_id: UUID
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }
    )


PagedExpense = Page[Expense]