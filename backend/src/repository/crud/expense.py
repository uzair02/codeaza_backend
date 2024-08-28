from uuid import UUID

import pendulum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config.settings.logger_config import logger
from src.models.db.expense import Expense as ExpenseModel
from src.models.schemas.expense import ExpenseCreate, ExpenseUpdate


async def create_expense(db: AsyncSession, user_id: UUID, expense: ExpenseCreate) -> ExpenseModel:
    """
    Create a new expense asynchronously.

    Args:
        db (AsyncSession): The database session.
        expense (ExpenseCreate): The expense data to create.

    Returns:
        ExpenseModel: The created expense model.

    Raises:
        RuntimeError: If there is an error creating the expense.
    """
    try:
        db_expense = ExpenseModel(
            subject=expense.subject,
            expense_date=expense.expense_date,
            reimbursable=expense.reimbursable,
            amount=expense.amount,
            description=expense.description,
            invoice_image=expense.invoice_image,
            employee=expense.employee,
            category_id=expense.category_id,
            user_id=user_id,
            updated_at=pendulum.now().naive(),
        )
        db.add(db_expense)
        await db.commit()
        await db.refresh(db_expense)
        logger.info(f"Expense created successfully with subject: {expense.subject}")
        return db_expense
    except Exception as e:
        logger.error(f"Error creating expense: {e}")
        raise RuntimeError("Error creating expense") from e


async def get_expense_by_id(db: AsyncSession, expense_id: UUID) -> ExpenseModel:
    """
    Retrieve an expense by ID asynchronously.

    Args:
        db (AsyncSession): The database session.
        expense_id (UUID): The ID of the expense to retrieve.

    Returns:
        ExpenseModel: The retrieved expense model.

    Raises:
        ValueError: If the expense is not found.
        RuntimeError: If there is an error retrieving the expense.
    """
    try:
        query = select(ExpenseModel).filter(ExpenseModel.expenses_id == expense_id)
        result = await db.execute(query)
        expense = result.scalars().first()
        if not expense:
            logger.warning(f"Expense not found with ID: {expense_id}")
            raise ValueError("Expense not found")
        logger.info(f"Expense retrieved successfully with ID: {expense_id}")
        return expense
    except ValueError as e:
        logger.error(f"Expense retrieval error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error retrieving expense with ID {expense_id}: {e}")
        raise RuntimeError("Error retrieving expense") from e


async def get_expenses(db: AsyncSession) -> list[ExpenseModel]:
    """
    Retrieve all expenses asynchronously.

    Args:
        db (AsyncSession): The database session.

    Returns:
        list[ExpenseModel]: The list of all expense models.

    Raises:
        RuntimeError: If there is an error retrieving the expenses.
    """
    try:
        query = select(ExpenseModel)
        result = await db.execute(query)
        expenses = list(result.scalars().all())
        logger.info(f"Total expenses retrieved: {len(expenses)}")
        return expenses
    except Exception as e:
        logger.error(f"Error retrieving expenses: {e}")
        raise RuntimeError("Error retrieving expenses") from e


async def update_expense(db: AsyncSession, expense_id: UUID, expense_update: ExpenseUpdate) -> ExpenseModel:
    """
    Update an expense by ID asynchronously.

    Args:
        db (AsyncSession): The database session.
        expense_id (UUID): The ID of the expense to update.
        expense_update (ExpenseUpdate): The expense data to update.

    Returns:
        ExpenseModel: The updated expense model.

    Raises:
        ValueError: If the expense is not found.
        RuntimeError: If there is an error updating the expense.
    """
    try:
        query = select(ExpenseModel).filter(ExpenseModel.expenses_id == expense_id)
        result = await db.execute(query)
        expense = result.scalars().first()
        if not expense:
            logger.warning(f"Expense not found with ID: {expense_id}")
            raise ValueError("Expense not found")

        if expense_update.subject is not None:
            expense.subject = expense_update.subject
        if expense_update.expense_date is not None:
            expense.expense_date = expense_update.expense_date
        if expense_update.amount is not None:
            expense.amount = expense_update.amount
        if expense_update.reimbursable is not None:
            expense.reimbursable = expense_update.reimbursable
        if expense_update.description is not None:
            expense.description = expense_update.description
        if expense_update.invoice_image is not None:
            expense.invoice_image = expense_update.invoice_image
        if expense_update.employee is not None:
            expense.employee = expense_update.employee

        expense.updated_at = pendulum.now().naive()

        await db.commit()
        await db.refresh(expense)
        logger.info(f"Expense updated successfully with ID: {expense_id}")
        return expense
    except ValueError as e:
        logger.error(f"Expense update error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error updating expense with ID {expense_id}: {e}")
        raise RuntimeError("Error updating expense") from e


async def delete_expense(db: AsyncSession, expense_id: UUID) -> bool:
    """
    Delete an expense by ID asynchronously.

    Args:
        db (AsyncSession): The database session.
        expense_id (UUID): The ID of the expense to delete.

    Returns:
        bool: True if the expense was deleted successfully.

    Raises:
        ValueError: If the expense is not found.
        RuntimeError: If there is an error deleting the expense.
    """
    try:
        query = select(ExpenseModel).filter(ExpenseModel.expenses_id == expense_id)
        result = await db.execute(query)
        expense = result.scalars().first()
        if not expense:
            logger.warning(f"Expense not found with ID: {expense_id}")
            raise ValueError("Expense not found")
        await db.delete(expense)
        await db.commit()
        logger.info(f"Expense deleted successfully with ID: {expense_id}")
        return True
    except ValueError as e:
        logger.error(f"Expense deletion error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error deleting expense with ID {expense_id}: {e}")
        raise RuntimeError("Error deleting expense") from e
