"""
Functions for working with expenses (add).
"""
import datetime
import gspread

from google_sheet.accounts import change_balance

service_account = gspread.service_account("google_token.json")


def get_expenses(worksheet: gspread.Worksheet) -> list:
    """
    Returns list of expenses (date, category, amount, account, description).

    :param worksheet: Google worksheet object.
    """
    dates = worksheet.col_values(1)[2:]
    categories = worksheet.col_values(2)[2:]
    amounts = worksheet.col_values(3)[2:]
    accounts = worksheet.col_values(4)[2:]
    descriptions = worksheet.col_values(5)[2:]

    expenses = []
    for i, date in enumerate(dates):
        expenses.append({
            "date": date,
            "category": categories[i],
            "amount": amounts[i],
            "account": accounts[i],
            "description": descriptions[i],
        })

    return expenses


def get_total_expenses(worksheet: gspread.Worksheet) -> int:
    """
    Returns number of expenses in table.

    :param worksheet: Google worksheet with expenses table.
    """
    return len(worksheet.col_values(1)[2:])


def add_expense(amount: float,
                category: str,
                account: str,
                comment: str,
                gsheet_id: str,
                total_expenses: int = None,
                account_names: list = None,
                accounts: dict = None):
    """
    Adds expens to Google sheet.

    :param amount: Money amount at account.
    :param category: Category of expense.
    :param account: Name of account.
    :param comment: Description to expense.
    :param gsheet_id: ID of Google sheet.
    :param total_expenses: Number of expenses in table.
    :param account_names: List of account names.
    :param accounts: Dict of account properties.

    :raise AssertionError: If amount less than 0.
    """
    sheet = service_account.open_by_key(gsheet_id)
    transactions_worksheet = sheet.worksheet("Транзакции")
    settings_worksheet = sheet.worksheet("Настройки")

    assert amount >= 0

    if total_expenses is None:
        total_expenses = get_total_expenses(transactions_worksheet)
        # total_expenses = len(get_expenses(transactions_worksheet))

    current_time = datetime.datetime.now()

    expenses = transactions_worksheet.get(f"A3:E{total_expenses + 2}")
    for row in expenses:
        if len(row) < 5:
            row += [""]

    transactions_worksheet.update(f"A4:E{total_expenses + 3}", expenses)
    transactions_worksheet.update("B3:E3", [[category, amount, account, comment]])
    transactions_worksheet.update_acell("A3", f"=date({current_time.year}, {current_time.month}, {current_time.day})")

    change_balance(
        "decrease",
        account,
        amount,
        account_names=account_names,
        accounts=accounts,
        worksheet=settings_worksheet,
    )
