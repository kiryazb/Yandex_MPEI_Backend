"""
Class Sheet for working with user's Google sheet.
"""
import gspread
import datetime

from google_sheet.categories import CategoriesSheet
from google_sheet.accounts import AccountsSheet


class Sheet:
    """Represents functions for working with user's Google sheet."""
    service_account = gspread.service_account("google_token.json")

    def __init__(self, gsheet_id: str):
        """
        :param gsheet_id: ID of user's Google sheet.
        """
        self.gsheet_id = gsheet_id

        self.sheet = self.service_account.open_by_key(gsheet_id)
        self.transactions_worksheet = self.sheet.worksheet("Транзакции")
        self.settings_worksheet = self.sheet.worksheet("Настройки")

        self.categories_sheet = CategoriesSheet(self.settings_worksheet)
        self.accounts_sheet = AccountsSheet(self.settings_worksheet)

        self.total_expenses = len(self.get_expenses())
        self.total_incomes = len(self.get_incomes())

    def add_expense(self, amount: float, category: str, account: str, comment: str = ""):
        """
        Adds expense to Google sheet.

        :param amount: Money amount at account.
        :param category: Category of expense.
        :param account: Name of account.
        :param comment: Description to expens.

        :raise AssertionError: If category does not exist or account does not exist or amount less than 0.
        """
        assert category in self.categories_sheet.categories["expense"]
        assert account in self.accounts_sheet.account_names
        assert amount >= 0

        current_time = datetime.datetime.now()

        self.sheet = self.service_account.open_by_key(self.gsheet_id)
        self.transactions_worksheet = self.sheet.worksheet("Транзакции")
        self.accounts_sheet.worksheet = self.sheet.worksheet("Настройки")

        transactions = self.transactions_worksheet.get(f"A3:E{self.total_expenses + 2}")
        for t_action in transactions:
            if len(t_action) < 5:
                t_action += [""]

        self.transactions_worksheet.update(
            f"A4:E{self.total_expenses + 3}",
            transactions
        )
        self.transactions_worksheet.update("B3:E3", [[category, amount, account, comment]])
        self.transactions_worksheet.update_acell(
            "A3", f"=date({current_time.year}, {current_time.month}, {current_time.day})"
        )

        self.total_expenses += 1

        # Update amount on account
        self.accounts_sheet.decrease_balance(account, amount)

    def add_income(self, amount: float, category: str, account: str, comment: str = ""):
        """
        Adds income to Google sheet.

        :param amount: Money amount at account.
        :param category: Category of income.
        :param account: Name of account.
        :param comment: Description to income.

        :raise AssertionError: If category does not exist or account does not exist or amount less than 0.
        """
        category = category.title()
        account = account.title()

        assert category in self.categories_sheet.categories["income"]
        assert account in self.accounts_sheet.account_names
        assert amount >= 0

        current_time = datetime.datetime.now()

        self.sheet = self.service_account.open_by_key(self.gsheet_id)
        self.transactions_worksheet = self.sheet.worksheet("Транзакции")
        self.accounts_sheet.worksheet = self.sheet.worksheet("Настройки")

        transactions = self.transactions_worksheet.get(f"G3:K{self.total_expenses + 2}")
        for t_action in transactions:
            if len(t_action) < 5:
                t_action += [""]

        self.transactions_worksheet.update(
            f"G4:K{self.total_expenses + 3}",
            transactions,
        )
        self.transactions_worksheet.update("H3:K3", [[category, amount, account, comment]])
        self.transactions_worksheet.update_acell(
            "G3", f"=date({current_time.year}, {current_time.month}, {current_time.day})"
        )

        self.total_incomes += 1

        # Update amount on account
        self.accounts_sheet.increase_balance(account, amount)

    def get_expenses(self) -> list:
        """Returns list of expenses (date, category, amount, account, description)."""
        ex_dates = self.transactions_worksheet.col_values(1)[2:]
        ex_categories = self.transactions_worksheet.col_values(2)[2:]
        ex_amounts = self.transactions_worksheet.col_values(3)[2:]
        ex_accounts = self.transactions_worksheet.col_values(4)[2:]
        ex_descriptions = self.transactions_worksheet.col_values(5)[2:]

        expenses = []
        for i, date in enumerate(ex_dates):
            expenses.append({
                "date": date,
                "category": ex_categories[i],
                "amount": ex_amounts[i],
                "account": ex_accounts[i],
                "description": ex_descriptions[i],
            })

        return expenses

    def get_incomes(self) -> list:
        """Returns list of incomes (date, category, amount, account, description)."""
        in_dates = self.transactions_worksheet.col_values(1)[2:]
        in_categories = self.transactions_worksheet.col_values(2)[2:]
        in_amounts = self.transactions_worksheet.col_values(3)[2:]
        in_accounts = self.transactions_worksheet.col_values(4)[2:]
        in_descriptions = self.transactions_worksheet.col_values(5)[2:]

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
