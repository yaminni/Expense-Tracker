import pytest
import pandas as pd
import os
from project.project import create, check, add_entry, delete_entry, update_entry, visualize_data

# Helper function to create an Excel file
def create_excel(file, content=None):
    if content is not None:
        df = pd.DataFrame(content)
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Type"])
    df.to_excel(file, sheet_name='Sheet1', index=False)

# Test create and initialization functions
def test_create_initialization():
    file = 'test_create_initialization.xlsx'
    if os.path.exists(file):
        os.remove(file)
    df = create(file)
    assert df.empty
    os.remove(file)

# Test adding an entry
def test_add_entry():
    file = 'test_add_entry.xlsx'
    create_excel(file)
    df = check(file)

    # Directly call the function with parameters instead of using input()
    date = '2024-08-01'
    category = 'Food'
    amount = 100
    entry_type = 'Income'

    df = add_entry(df, file, date, category, amount, entry_type)
    assert len(df) == 1
    assert df.iloc[0]['Date'] == '2024-08-01'
    assert df.iloc[0]['Category'] == 'Food'
    assert df.iloc[0]['Amount'] == 100.0
    assert df.iloc[0]['Type'] == 'Income'
    os.remove(file)

# Test deleting an entry
def test_delete_entry():
    file = 'test_delete_entry.xlsx'
    create_excel(file, [{'Date': '2024-08-01', 'Category': 'Food', 'Amount': 100, 'Type': 'Income'}])
    df = check(file)

    # Directly call the function with parameters instead of using input()
    date = '2024-08-01'
    category = 'Food'
    amount = 100
    entry_type = 'Income'

    df = delete_entry(df, file, date, category, amount, entry_type)
    assert df.empty
    os.remove(file)

# Test updating an entry
def test_update_entry():
    file = 'test_update_entry.xlsx'
    create_excel(file, [{'Date': '2024-08-01', 'Category': 'Food', 'Amount': 100, 'Type': 'Income'}])
    df = check(file)

    # Directly call the function with parameters instead of using input()
    old_date = '2024-08-01'
    old_category = 'Food'
    old_amount = 100
    old_entry_type = 'Income'

    new_date = '2024-08-02'
    new_category = 'Rent'
    new_amount = 200
    new_entry_type = 'Expense'

    df = update_entry(df, file, old_date, old_category, old_amount, old_entry_type, new_date, new_category, new_amount, new_entry_type)
    assert len(df) == 1
    assert df.iloc[0]['Date'] == '2024-08-02'
    assert df.iloc[0]['Category'] == 'Rent'
    assert df.iloc[0]['Amount'] == 200.0
    assert df.iloc[0]['Type'] == 'Expense'
    os.remove(file)

if __name__ == "__main__":
    pytest.main()
