"""
Functions for working with accounts (add, delete, rename, change_balance, change_type (savings or not)).
"""
import gspread


service_account = gspread.service_account("google_token.json")


def get_account_names(sheet: gspread.spreadsheet.Spreadsheet) -> list:
    """
    Returns dict of accounts.

    :param sheet: Goolge sheet object.
    """
    worksheet = sheet.get_worksheet(1)

    accounts = list()
    for acc_name in worksheet.col_values(5)[3:]:
        accounts.append(acc_name.title())

    return accounts


def get_accounts(worksheet: gspread.Worksheet = None, gsheet_id: str = None) -> (list, dict):
    """
    Returns dict with accounts. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param worksheet: Google worksheet with accounts table.
    :param gsheet_id: ID of user's Google sheet.

    :raise ValueError: If no one of the parameters (worksheet or gsheet_id) were passed to the function.
        If changing_type is not decrease, increase or set.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    names = worksheet.col_values(5)[3:]
    amounts = worksheet.col_values(6)[3:]
    # is_savings = worksheet.col_values(7)[3:]

    acc_names, accounts = list(), dict()
    for i, name in enumerate(names):
        acc_names.append(name)
        accounts[name.lower()] = {
            "name": name,
            "amount": float(amounts[i].split()[0].replace(",", "")),
            # "is_saving": True if is_savings[i].lower() == "true" else False
        }

    return acc_names, accounts


def add_account(name: str,
                amount: float,
                accounts: dict = None,
                account_names: list = None,
                gsheet_id: str = None,
                worksheet: gspread.Worksheet = None):
    """
    Adds account to list. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

        :param name: Account name.
        :param amount: New amount on account.
        :param account_names: List of account names.
        :param accounts: Dict of account properties.
        :param gsheet_id: ID of Google sheet.
        :param worksheet: Google sheet with accounts table.

    :raise ValueError: If account with acc_name already exists.
        If no one of the parameters (worksheet or gsheet_id) were passed to the function.
    :raise AssertionError: If amount type is not float or int.
    """
    assert type(amount) in [int, float]

    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    if accounts is None or account_names is None:
        account_names, accounts = get_accounts(worksheet)

    if name.lower() in accounts:
        raise ValueError(f"Account with name {name} already exists!")

    last_row = len(accounts) + 4
    worksheet.update(f"E{last_row}:F{last_row}", [[name, amount]])
    # Cahnging shape format.
    resize_shape(last_row, "increase", worksheet)


def rename_account(name: str,
                   new_name: str,
                   account_names: list = None,
                   gsheet_id: str = None,
                   worksheet: gspread.Worksheet = None):
    """
    Renames account with name to new_name. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param name: Account name.
    :param new_name: New account name.
    :param account_names: List of account names.
    :param gsheet_id: ID of Google sheet.
    :param worksheet: Google sheet with accounts table.

    :raise ValueError: if account with acc_name does not exist. If account with acc_name already exists.
        If no one of the parameters (worksheet or gsheet_id) were passed to the function.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    if account_names is None:
        account_names, _ = get_accounts(worksheet)

    lowercase_account_names = list(map(lambda word: word.lower(), account_names))
    if name.lower() not in lowercase_account_names:
        raise ValueError(f"Account with name {name} does not exist!")

    if new_name.lower() in lowercase_account_names:
        raise ValueError(f"It is imposible to rename {name} account to {new_name} "
                         f"because accouunt with {new_name} already exist!")

    worksheet.update(f"E{lowercase_account_names.index(name) + 1 + 3}", new_name)


def change_balance(changing_type: str,
                   acc_name: str,
                   amount: float,
                   accounts: dict = None,
                   account_names: list = None,
                   gsheet_id: str = None,
                   worksheet: gspread.Worksheet = None):
    """
    Changes account's balance. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param changing_type: Must be increase/decrease/set
    :param acc_name: Account name.
    :param amount: New amount on account.
    :param account_names: List of account names.
    :param accounts: Dict of account properties.
    :param gsheet_id: ID of Google sheet.
    :param worksheet: Google sheet with accounts table.

    :raise AssertionError: If account with acc_name does not exist.
    :raise ValueError: If no one of the parameters (worksheet or gsheet_id) were passed to the function.
        If changing_type is not decrease, increase or set.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    if accounts is None or account_names is None:
        account_names, accounts = get_accounts(worksheet)

    lower_account_names = list(map(lambda word: word.lower(), account_names))
    assert acc_name.lower() in lower_account_names

    if changing_type == "set":
        worksheet.update(f"F{lower_account_names.index(acc_name.lower()) + 1 + 3}", amount)
    elif changing_type in ["increase", "decrease"]:
        if changing_type == "decrease":
            amount *= -1

        worksheet.update(
            f"F{lower_account_names.index(acc_name.lower()) + 1 + 3}",
            accounts[acc_name.lower()]["amount"] + amount,
        )

    else:
        raise ValueError(f"changing_type must be increase/decrease/set but not {changing_type}")


def delete_account(name: str,
                   account_names: list = None,
                   gsheet_id: str = None,
                   worksheet: gspread.Worksheet = None):
    """
    Deletes account with passed name.One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param name: Account name.
    :param account_names: List of account names.
    :param gsheet_id: ID of Google sheet.
    :param worksheet: Google sheet with accounts table.

    :raise ValueError: If no one of the parameters (worksheet or gsheet_id) were passed to the function.
        If account with name does not exist.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    if account_names is None:
        account_names, _ = get_accounts(worksheet)

    lowercase_account_names = list(map(lambda word: word.lower(), account_names))
    if name.lower() not in lowercase_account_names:
        raise ValueError(f"Account with name {name} does not exist!")

    row_index = lowercase_account_names.index(name.lower()) + 1 + 3

    # Moving accounts up.
    num_accounts = len(account_names)
    worksheet.update(
        f"E{row_index}:G{num_accounts + 3}",
        worksheet.get(
            f"E{row_index + 1}:G{num_accounts + 3}"
        )
    )
    worksheet.update(f"E{num_accounts + 3}:G{num_accounts + 3}", [["", "", ""]])

    # Changing shape format.
    resize_shape(num_accounts + 4, "decrease", worksheet)


def resize_shape(last_row: int, direct: str, worksheet: gspread.worksheet.Worksheet):
    """
    Resizes accounts shape in Google sheet.

    :param last_row: Index of the last row into categories table (rows starts woth 1).
    :param direct: Direction of resizing. Must be increase or decrease.
    :param worksheet: Worksheet in Google sheets.

    :raise ValueError: If direct not increase/decrease.
    :raise AssertionError: If last_row less than 1.
    """
    assert last_row >= 1

    def set_bottom(row_index: int):
        """
        Sets the bottom of the shape. |__|__|__|.

        :param row_index: Index of the row in Google sheet (starts with 1).

        :raise AssertionError: If row_index less than 1.
        """
        assert row_index >= 1

        worksheet.format(
            f"E{row_index}",
            {
                "borders": {
                    "left": {
                        "style": "SOLID_MEDIUM",
                    },
                    "right": {
                        "style": "DOTTED",
                    },
                    "bottom": {
                        "style": "SOLID_MEDIUM",
                    }
                }
            }
        )
        worksheet.format(
            f"F{row_index}",
            {
                "borders": {
                    "left": {
                        "style": "DOTTED",
                    },
                    "right": {
                        "style": "SOLID_MEDIUM",
                    },
                    "bottom": {
                        "style": "SOLID_MEDIUM",
                    }
                }
            }
        )
        # worksheet.format(
        #     f"F{row_index}",
        #     {
        #         "borders": {
        #             "left": {
        #                 "style": "DOTTED",
        #             },
        #             "right": {
        #                 "style": "DOTTED",
        #             },
        #             "bottom": {
        #                 "style": "SOLID_MEDIUM",
        #             }
        #         }
        #     }
        # )
        # worksheet.format(
        #     f"G{row_index}",
        #     {
        #         "borders": {
        #             "left": {
        #                 "style": "DOTTED",
        #             },
        #             "right": {
        #                 "style": "SOLID_MEDIUM",
        #             },
        #             "bottom": {
        #                 "style": "SOLID_MEDIUM",
        #             }
        #         }
        #     }
        # )

    if direct == "increase":
        worksheet.format(
            f"E{last_row}",
            {
                "borders": {
                    "left": {
                        "style": "SOLID_MEDIUM",
                    },
                    "right": {
                        "style": "DOTTED",
                    }
                }
            }
        )
        worksheet.format(
            f"F{last_row}",
            {
                "borders": {
                    "right": {
                        "style": "SOLID_MEDIUM",
                    },
                    "left": {
                        "style": "DOTTED",
                    }
                }
            }
        )
        # worksheet.format(
        #     f"F{last_row}",
        #     {
        #         "borders": {
        #             "left": {
        #                 "style": "DOTTED",
        #             },
        #             "right": {
        #                 "style": "DOTTED",
        #             }
        #         }
        #     }
        # )
        # worksheet.format(
        #     f"G{last_row}",
        #     {
        #         "borders": {
        #             "right": {
        #                 "style": "SOLID_MEDIUM",
        #             },
        #             "left": {
        #                 "style": "DOTTED",
        #             }
        #         }
        #     }
        # )
        set_bottom(last_row + 1)

    elif direct == "decrease":
        worksheet.format(f"E{last_row}:G{last_row}", {"borders": {}})
        set_bottom(last_row - 1)

    else:
        raise ValueError(f"direct param must be increase or decrease but not {direct}!")
