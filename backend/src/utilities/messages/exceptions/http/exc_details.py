from uuid import UUID


### Details for Category
def category_not_found(category_id: UUID) -> str:
    return f"No category found with ID '{category_id}'. Please check the ID and try again."


def category_not_found_by_name(name: str) -> str:
    return f"No category found with the name '{name}'. Please check the name and try again."


def category_exists(name: str) -> str:
    return f"Category with name '{name}' already exists. Please choose a different name."


def category_update_not_found(category_id: UUID) -> str:
    return f"No category found with ID '{category_id}' for update. Please check the ID and try again."


def category_deletion_not_found(category_id: UUID) -> str:
    return f"No category found with ID '{category_id}' for deletion. Please check the ID and try again."


def unexpected_error_create(name: str) -> str:
    return f"An unexpected error occurred while creating the category '{name}'. Please try again later."


def unexpected_error_retrieve_by_id(category_id: UUID) -> str:
    return (
        f"An unexpected error occurred while retrieving the category with ID '{category_id}'. Please try again later."
    )


def unexpected_error_retrieve_by_name(name: str) -> str:
    return f"An unexpected error occurred while retrieving the category with name '{name}'. Please try again later."


def unexpected_error_update(category_id: UUID) -> str:
    return f"An unexpected error occurred while updating the category with ID '{category_id}'. Please try again later."


def unexpected_error_delete(category_id: UUID) -> str:
    return f"An unexpected error occurred while deleting the category with ID '{category_id}'. Please try again later."


def unexpected_error_list() -> str:
    return "An unexpected error occurred while retrieving the list of categories. Please try again later."


### Details for Expenses
def expense_not_found(expense_id: UUID) -> str:
    return f"No expense found with ID '{expense_id}'. Please check the ID and try again."


def expense_exists(name: str) -> str:
    return f"Expense with name '{name}' already exists. Please choose a different name."


def expense_update_not_found(expense_id: UUID) -> str:
    return f"No expense found with ID '{expense_id}' for update. Please check the ID and try again."


def expense_deletion_not_found(expense_id: UUID) -> str:
    return f"No expense found with ID '{expense_id}' for deletion. Please check the ID and try again."


def expense_unexpected_error_create(subject: str) -> str:
    return f"An unexpected error occurred while creating the expense '{subject}'. Please try again later."


def expense_unexpected_error_retrieve_by_id(expense_id: UUID) -> str:
    return f"An unexpected error occurred while retrieving the expense with ID '{expense_id}'. Please try again later."


def expense_unexpected_error_retrieve_by_name(name: str) -> str:
    return f"An unexpected error occurred while retrieving the expense with name '{name}'. Please try again later."


def expense_unexpected_error_update(expense_id: UUID) -> str:
    return f"An unexpected error occurred while updating the expense with ID '{expense_id}'. Please try again later."


def expense_unexpected_error_delete(expense_id: UUID) -> str:
    return f"An unexpected error occurred while deleting the expense with ID '{expense_id}'. Please try again later."


def expense_unexpected_error_list() -> str:
    return "An unexpected error occurred while retrieving the list of expenses. Please try again later."
