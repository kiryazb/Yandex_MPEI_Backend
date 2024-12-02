"""
Functions for working with incomes (add).
"""
import datetime
import gspread

from google_sheet.accounts import change_balance

service_account = gspread.service_account("google_token.json")


def get_incomes(sheet: gspread.spreadsheet.Spreadsheet) -> list:
    """
    Returns list of incomes (date, category, amount, account, description).

    :param sheet: Google sheet object.
    """
    worksheet = sheet.get_worksheet(0)

    in_dates = worksheet.col_values(1)[2:]
    in_categories = worksheet.col_values(2)[2:]
    in_amounts = worksheet.col_values(3)[2:]
    in_accounts = worksheet.col_values(4)[2:]
    in_descriptions = worksheet.col_values(5)[2:]

    incomes = []
    for i, date in enumerate(in_dates):
        incomes.append({
            "date": date,
            "category": in_categories[i],
            "amount": in_amounts[i],
            "account": in_accounts[i],
            "description": in_descriptions[i],
        })

    return incomes


def get_total_incomes(worksheet: gspread.Worksheet) -> int:
    """
    Returns number of incomes in table.

    :param worksheet: Google worksheet with incomes table.
    """
    return len(worksheet.col_values(7)[2:])


def add_income(amount: float,
               category: str,
               account: str,
               comment: str,
               gsheet_id: str,
               total_incomes: int = None,
               account_names: list = None,
               accounts: dict = None):
    """
    Adds income to Google sheet.

    :param amount: Money amount at account.
    :param category: Category of income.
    :param account: Name of account.
    :param gsheet_id: ID of Google sheet.
    :param comment: Description to income.
    :param total_incomes: Number of incomes in table.
    :param account_names: List of account names.
    :param accounts: Dict of account properties.

    :raise AssertionError: If category does not exist or account does not exist or amount less than 0.
    """
    sheet = service_account.open_by_key(gsheet_id)
    transactions_worksheet = sheet.worksheet("Транзакции")
    settings_worksheet = sheet.worksheet("Настройки")

    assert amount >= 0

    if total_incomes is None:
        total_incomes = get_total_incomes(transactions_worksheet)

    current_time = datetime.datetime.now()

    incomes = transactions_worksheet.get(f"G3:K{total_incomes + 2}")
    for row in incomes:
        if len(row) < 5:
            row += [""]

    transactions_worksheet.update(f"G4:K{total_incomes + 3}", incomes)
    transactions_worksheet.update("H3:K3", [[category, amount, account, comment]])
    transactions_worksheet.update_acell("G3", f"=date({current_time.year}, {current_time.month}, {current_time.day})")

    change_balance(
        "increase",
        account,
        amount,
        account_names=account_names,
        accounts=accounts,
        worksheet=settings_worksheet,
    )
