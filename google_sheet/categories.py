"""
Functions for working with categories (add, rename, delete).
"""
import logging
import gspread


service_account = gspread.service_account("google_token.json")


def get_categories(worksheet: gspread.Worksheet = None, gsheet_id: str = None) -> dict:
    """
    Returns all categories of expense/income. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param gsheet_id: ID of user's Google sheet.
    :param worksheet: Goolge worksheet object.

    :raise ValueError: If no one of the parameters (worksheet or gsheet_id) were passed to the function.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            logging.info(f"Connecting to gsheet with key: {gsheet_id}")
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    categories = dict()
    categories["expense"] = worksheet.col_values(2)[3:]
    categories["income"] = worksheet.col_values(3)[3:]

    return categories


def add_category(cat_name: str,
                 cat_type: str,
                 categories: dict = None,
                 gsheet_id: str = None,
                 worksheet: gspread.Worksheet = None):
    """
    Adds category to list. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param cat_name: Name of new category.
    :param cat_type: Type of catrgory (expense/income).
    :param categories: Dict of expense/income categories.
    :param gsheet_id: ID of user's Google sheet.
    :param worksheet: Google worksheet with category table.

    :raise ValueError: If category with cat_name already exists.
        If cat_type not income/expense.
        If no one of the parameters (worksheet or gsheet_id) were passed to the function.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    if categories is None:
        categories = get_categories(worksheet=worksheet)

    cat_type = cat_type.lower()
    if cat_type not in ["expense", "income"]:
        raise ValueError(f"cat_type must be income or expense but not {cat_type}!")

    if cat_name.lower() in map(lambda word: word.lower(), categories[cat_type]):
        raise ValueError(f"{cat_type.title()} category with name {cat_name} already exist!")

    num_expense_cats = len(categories["expense"])
    num_income_cats = len(categories["income"])

    # Adding category to sheet
    if cat_type == "expense":
        last_row = num_expense_cats + 4
        worksheet.update(f"B{last_row}", cat_name)

    else:  # cat_type = income
        last_row = num_income_cats + 4
        worksheet.update(f"C{last_row}", cat_name)

    # Changing border format
    if (num_expense_cats == num_income_cats or
            num_expense_cats > num_income_cats and cat_type == "expense" or
            num_expense_cats < num_income_cats and cat_type == "income"):
        resize_shape(last_row, "increase", worksheet)


def rename_category(cat_name: str,
                    new_cat_name: str,
                    cat_type: str,
                    categories: dict = None,
                    gsheet_id: str = None,
                    worksheet: gspread.Worksheet = None):
    """
    Renames a category with cat_name to new_cat_name. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param cat_name: Name of category.
    :param new_cat_name: Name in which category with cat_name will be renamed.
    :param cat_type: Type of catrgory (expense/income).
    :param categories: Dict of expense/income categories.
    :param gsheet_id: ID of google sheet.
    :param worksheet: Google worksheet with categories table.

    :raise ValueError: if category with cat_name does not exist or
        category with new_cat_name already exist.
        If cat_type not income/expense.
        If no one of the parameters (worksheet or gsheet_id) were passed to the function.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    cat_type = cat_type.lower()
    if cat_type == "expense":
        cell_index = "B"
    elif cat_type == "income":
        cell_index = "C"
    else:
        raise ValueError(f"cat_type must be income or expense but not {cat_type}!")

    if categories is None:
        categories = get_categories(worksheet=worksheet)[cat_type]

    lowercase_categories = dict()
    lowercase_categories["expense"] = list(map(lambda word: word.lower(), categories["expense"]))
    lowercase_categories["income"] = list(map(lambda word: word.lower(), categories["income"]))

    if cat_name.lower() not in lowercase_categories[cat_type]:
        raise ValueError(f"{cat_type.title()} category with name {cat_name} does not exist!")
    if new_cat_name.lower() in lowercase_categories[cat_type]:
        raise ValueError(f"It is imposible to rename {cat_name} category to {new_cat_name} because "
                         f"category with {new_cat_name} already exist!")

    cell_index += str(lowercase_categories[cat_type].index(cat_name.lower()) + 1 + 3)
    worksheet.update(cell_index, new_cat_name)


def delete_category(cat_name: str,
                    cat_type: str,
                    categories: dict = None,
                    gsheet_id: str = None,
                    worksheet: gspread.Worksheet = None):
    """
    Deletes cat_type category with name cat_name. One of the parameters must be passed to the function
    (worksheet or gsheet_id) otherwise ValueError.

    :param cat_name: Name of category.
    :param cat_type: Type of catrgory (expense/income).
    :param categories: Dict of categories.
    :param gsheet_id: ID of Google sheet.
    :param worksheet: Google worksheet with categories table.

    :raise ValueError: If category with cat_name does not exist.
        If cat_type not income/expense. If no one of
        the parameters (worksheet or gsheet_id) were passed to the function.
    """
    if worksheet is None:
        if gsheet_id is None:
            raise ValueError("No one of the parameters (sheet or gsheet_id) were passed to the function!")
        else:
            sheet = service_account.open_by_key(gsheet_id)
            worksheet = sheet.worksheet("Настройки")

    cat_type = cat_type.lower()
    if cat_type == "expense":
        col_index = "B"
    elif cat_type == "income":
        col_index = "C"
    else:
        raise ValueError(f"cat_type must be income or expense but not {cat_type}!")

    if categories is None:
        categories = get_categories(worksheet=worksheet)

    lowercase_categories = dict()
    lowercase_categories["expense"] = list(map(lambda word: word.lower(), categories["expense"]))
    lowercase_categories["income"] = list(map(lambda word: word.lower(), categories["income"]))

    if cat_name.lower() not in lowercase_categories[cat_type]:
        raise ValueError(f"{cat_type.title()} category with name {cat_name} does not exist!")

    row_index = lowercase_categories[cat_type].index(cat_name.lower()) + 1 + 3

    # Moving categories up.
    worksheet.update(
        f"{col_index}{row_index}:{col_index}{len(categories[cat_type]) + 3}",
        worksheet.get(
            f"{col_index}{row_index + 1}:{col_index}{len(categories[cat_type]) + 3}"
        )
    )
    worksheet.update(f"{col_index}{len(categories[cat_type]) + 3}", "")

    if (len(categories["expense"]) == len(categories["income"]) or
            len(categories["expense"]) > len(categories["income"]) and cat_type == "expense" or
            len(categories["income"]) > len(categories["expense"]) and cat_type == "income"):
        resize_shape(len(categories[cat_type]) + 4, "decrease", worksheet)


def resize_shape(last_row: int, direct: str, worksheet: gspread.worksheet.Worksheet):
    """
    Resizes categories shape in Google sheet.

    :param last_row: Index of the last row into categories table (rows starts woth 1).
    :param direct: Direction of resizing. Must be increase or decrease.
    :param worksheet: Worksheet in Google sheets.

    :raise ValueError: If direct not increase/decrease.
    :raise AssertionError: If last_row less than 1.
    """
    assert last_row >= 1

    def set_bottom(row_index: int):
        """
        Sets the bottom of the shape. |__|__|.

        :param row_index: Index of the row in Google sheet (starts with 1).

        :raise AssertionError: If row_index less than 1.
        """
        assert row_index >= 1

        worksheet.format(
            f"B{row_index}",
            {
                "borders": {
                    "left": {
                        "style": "SOLID_MEDIUM",
                    },
                    "right": {
                        "style": "DASHED",
                    },
                    "bottom": {
                        "style": "SOLID_MEDIUM",
                    }
                }
            }
        )
        worksheet.format(
            f"C{row_index}",
            {
                "borders": {
                    "left": {
                        "style": "DASHED",
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

    if direct == "increase":
        worksheet.format(
            f"B{last_row}",
            {
                "borders": {
                    "left": {
                        "style": "SOLID_MEDIUM",
                    },
                    "right": {
                        "style": "DASHED",
                    }
                }
            }
        )
        worksheet.format(
            f"C{last_row}",
            {
                "borders": {
                    "right": {
                        "style": "SOLID_MEDIUM",
                    },
                    "left": {
                        "style": "DASHED",
                    }
                }
            }
        )
        set_bottom(last_row + 1)

    elif direct == "decrease":
        worksheet.format(f"B{last_row}:C{last_row}", {"borders": {}})
        set_bottom(last_row - 1)

    else:
        raise ValueError(f"direct param must be increase or decrease but not {direct}!")
