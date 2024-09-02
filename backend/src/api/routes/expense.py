from uuid import UUID
from typing import Optional
import json
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi_pagination import add_pagination, paginate, Params
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings.logger_config import logger
from src.models.schemas.error_response import ErrorResponse
from src.models.schemas.expense import Expense as ExpenseSchema, ExpenseCreate, ExpenseUpdate, PagedExpense
from src.models.schemas.user import User
from src.repository.crud.expense import create_expense, delete_expense, get_expense_by_id, get_expenses, update_expense
from src.repository.database import get_db
from src.securities.verification.credentials import get_current_user
from src.utilities.messages.exceptions.http.exc_details import (
    expense_deletion_not_found,
    expense_not_found,
    expense_unexpected_error_create,
    expense_unexpected_error_delete,
    expense_unexpected_error_list,
    expense_unexpected_error_retrieve_by_id,
    expense_unexpected_error_update,
    expense_update_not_found,
)

router = APIRouter()


@router.post(
    "/expenses",
    response_model=ExpenseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_expense_endpoint(
    expense: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    invoice_image: Optional[UploadFile] = File(None)
) -> ExpenseSchema:
    """
    Create a new expense.

    Args:
        expense (str): The expense data to create, as a JSON string.
        current_user (User): The current authenticated user.
        db (AsyncSession): The database session.
        invoice_image (UploadFile, optional): The invoice image file.

    Returns:
        ExpenseSchema: The created expense object.
    """
    try:
        # Parse the expense data from the JSON string
        expense_data = json.loads(expense)
        expense_obj = ExpenseCreate(**expense_data)

        db_expense = await create_expense(db, current_user.user_id, expense_obj, invoice_image)
        logger.info(f"Expense created successfully with ID: {db_expense.expenses_id}")
        return ExpenseSchema.model_validate(db_expense)
    except ValueError as e:
        logger.error(f"Error creating expense: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                detail=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            ).model_dump(),
        ) from e
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in expense data: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                detail="Invalid JSON in expense data",
                status_code=status.HTTP_400_BAD_REQUEST,
            ).model_dump(),
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error during expense creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                detail=expense_unexpected_error_create(expense_obj.subject),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ).model_dump(),
        ) from e


@router.get(
    "/expenses",
    response_model=PagedExpense,
    responses={
        500: {"model": ErrorResponse},
    },
)
async def list_expenses_endpoint(
    db: AsyncSession = Depends(get_db),
    params: Params = Depends(),
    current_user: User = Depends(get_current_user),
) -> PagedExpense:
    """
    Retrieve expenses with pagination.

    Args:
        db (AsyncSession): The database session.
        params (Params): Pagination parameters.

    Returns:
        PagedExpense: A paginated response containing expenses.
    """
    try:
        logger.info("Fetching expenses with pagination")
        expenses = await get_expenses(db)
        return paginate(expenses, params)
    except Exception as e:
        logger.error(f"Unexpected error while retrieving expenses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                detail=expense_unexpected_error_list(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ).dict(),
        ) from e


@router.get(
    "/expenses/{expense_id}",
    response_model=ExpenseSchema,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_expense_endpoint(
    expense_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ExpenseSchema:
    """
    Retrieve an expense by ID.

    Args:
        expense_id (UUID): The ID of the expense to retrieve.
        db (Session): The database session.

    Returns:
        ExpenseSchema: The retrieved expense object.
    """
    try:
        logger.info(f"Fetching expense with ID: {expense_id}")
        db_expense = await get_expense_by_id(db, expense_id)
        return ExpenseSchema.from_orm(db_expense)
    except ValueError as e:
        logger.error(f"Error retrieving expense with ID {expense_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                detail=expense_not_found(expense_id),
                status_code=status.HTTP_404_NOT_FOUND,
            ).dict(),
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error while retrieving expense with ID {expense_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                detail=expense_unexpected_error_retrieve_by_id(expense_id),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ).dict(),
        ) from e


@router.put(
    "/expenses/{expense_id}",
    response_model=ExpenseSchema,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_expense_endpoint(
    expense_id: UUID,
    expense_update: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    invoice_image: Optional[UploadFile] = File(None)
) -> ExpenseSchema:
    """
    Update an existing expense.

    Args:
        expense_id (UUID): The ID of the expense to update.
        expense_update (str): JSON string of the updated expense data.
        current_user (User): The current authenticated user.
        db (AsyncSession): The database session.
        invoice_image (UploadFile, optional): The invoice image file.

    Returns:
        ExpenseSchema: The updated expense object.
    """
    try:
        expense_update_data = json.loads(expense_update)
        expense_update_obj = ExpenseUpdate(**expense_update_data)

        logger.info(f"Attempting to update expense with ID: {expense_id}")
        db_expense = await update_expense(db, expense_id, expense_update_obj, invoice_image)
        return ExpenseSchema.from_orm(db_expense)
    except ValueError as e:
        logger.error(f"Error updating expense with ID {expense_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                detail=expense_update_not_found(expense_id),
                status_code=status.HTTP_404_NOT_FOUND,
            ).dict(),
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error while updating expense with ID {expense_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                detail=expense_unexpected_error_update(expense_id),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ).dict(),
        ) from e


@router.delete(
    "/expenses/{expense_id}",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_expense_endpoint(
    expense_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Delete an expense by ID.

    Args:
        expense_id (UUID): The ID of the expense to delete.
        db (Session): The database session.

    Returns:
        dict: A message indicating the result of the deletion.
    """
    try:
        logger.info(f"Attempting to delete expense with ID: {expense_id}")
        result = await delete_expense(db, expense_id)
        return {"message": "Expense deleted successfully", "result": result}
    except ValueError as e:
        logger.error(f"Error deleting expense with ID {expense_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                detail=expense_deletion_not_found(expense_id),
                status_code=status.HTTP_404_NOT_FOUND,
            ).dict(),
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error while deleting expense with ID {expense_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                detail=expense_unexpected_error_delete(expense_id),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ).dict(),
        ) from e


add_pagination(router)
