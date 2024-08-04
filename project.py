import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

def main():
    #asking the user to select one from the two options
    print("HELLO!!\n1. NEW USER\n2. EXISTING USER\n")
    try:
        select = int(input("SELECT 1 OR 2: "))
        if select not in [1, 2]:
            sys.exit("Invalid selection")
    except ValueError:
        sys.exit("Invalid selection")

    file = input("FILE NAME (without extension): ") + ".xlsx"

    #If the user select 1 then program will implement create function to create a new file
    if select == 1:
        df = create(file)
    #If the user select 2 then program will implemnt check function whether the file exist or not
    elif select == 2:
        df = check(file)

    #asking the user about the task they wanna perform
    while True:
        print("\nOptions:")
        print("1. Add Income or Expense")
        print("2. Delete Entry")
        print("3. Update Entry")
        print("4. Track Through Chart")
        print("5. Exit")
        choice = input("Select an option (1-5): ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Food, Rent): ").capitalize()
            amount = float(input("Enter amount: "))
            entry_type = input("Enter type (Income/Expense): ").capitalize()
            df = add_entry(df, file, date, category, amount, entry_type)
        elif choice == '2':
            date = input("Enter date of entry to delete (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Food, Rent): ").capitalize()
            amount = float(input("Enter amount: "))
            entry_type = input("Enter type of entry to delete (Income/Expense): ").capitalize()
            df = delete_entry(df, file, date, category, amount, entry_type)
        elif choice == '3':
            old_date = input("Enter date of entry to update (YYYY-MM-DD): ")
            old_category = input("Enter category of the entry to update (e.g., Food, Rent): ").capitalize()
            old_amount = float(input("Enter amount of the entry to update: "))
            old_entry_type = input("Enter type of entry to update (Income/Expense): ").capitalize()
            new_date = input("Enter new date (YYYY-MM-DD): ")
            new_category = input("Enter new category (e.g., Food, Rent): ").capitalize()
            new_amount = float(input("Enter new amount: "))
            new_entry_type = input("Enter new type (Income/Expense): ").capitalize()
            df = update_entry(df, file, old_date, old_category, old_amount, old_entry_type, new_date, new_category, new_amount, new_entry_type)
        elif choice == '4':
            visualize_data(df)
        elif choice == '5':
            sys.exit("Have a nice day!")
        else:
            print("Invalid option. Please try again.")

#this function is used to create new file if there is no existing file with same name
def create(file):
    if not os.path.exists(file):
        return initialize(file)
    else:
        ask = input("Did you mean existing file? (answer Yes or No) ")
        if ask.lower().strip() in ["yes", "no"]:
            if ask.lower().strip() == "yes":
                return check(file)
            else:
                sys.exit("Choose another name")
        else:
            raise ValueError("Invalid selection")

#If there no existing file then this function below will initiate new file
def initialize(file):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Type"])
    df.to_excel(file, sheet_name='Sheet1', index=False)
    return df

#this function check if the file exist or not
def check(file):
    if os.path.exists(file):
        return pd.read_excel(file, sheet_name='Sheet1')
    else:
        sys.exit("File does not exist. Please create a new file.")

#This function ensure to add data to the existing file in excel
def add_entry(df, file, date, category, amount, entry_type):
    try:
        if entry_type not in ['Income', 'Expense']:
            raise ValueError("Entry type must be 'Income' or 'Expense'")

        new_entry = pd.DataFrame([{'Date': date, 'Category': category, 'Amount': amount, 'Type': entry_type}])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(file, sheet_name='Sheet1', index=False)
        print("Entry added successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    return df

#This function ensure to delete data from the existing file
def delete_entry(df, file, date, category, amount, entry_type):
    try:
        if entry_type not in ['Income', 'Expense']:
            raise ValueError("Entry type must be 'Income' or 'Expense'")

        date = pd.to_datetime(date).strftime('%Y-%m-%d')
        index_to_delete = df[(df['Date'] == date) & (df['Type'] == entry_type) & (df['Category'] == category) & (df['Amount'] == amount)].index

        if index_to_delete.empty:
            print("No matching entry found to delete.")
        else:
            df.drop(index_to_delete, inplace=True)
            df.to_excel(file, sheet_name='Sheet1', index=False)
            print("Entry deleted successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    return df

#This function ensure to update values in the existing file
def update_entry(df, file, old_date, old_category, old_amount, old_entry_type, new_date, new_category, new_amount, new_entry_type):
    try:
        if old_entry_type not in ['Income', 'Expense'] or new_entry_type not in ['Income', 'Expense']:
            raise ValueError("Entry type must be 'Income' or 'Expense'")

        old_date = pd.to_datetime(old_date).strftime('%Y-%m-%d')
        index_to_update = df[(df['Date'] == old_date) & (df['Type'] == old_entry_type) & (df['Category'] == old_category) & (df['Amount'] == old_amount)].index

        if index_to_update.empty:
            print("No matching entry found to update.")
        else:
            df.loc[index_to_update, ['Date', 'Category', 'Amount', 'Type']] = [new_date, new_category, new_amount, new_entry_type]
            df.to_excel(file, sheet_name='Sheet1', index=False)
            print("Entry updated successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    return df

#This function ensure to visualize the dataset of the existing file
def visualize_data(df):
    if df.empty:
        print("No data to visualize.")
        return

    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

    grouped_df = df.groupby(['Category', 'Type'])['Amount'].sum().unstack().fillna(0)

    ax = grouped_df.plot(kind='bar', stacked=True, figsize=(10, 7))
    plt.title('Income and Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.legend(title='Type')
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()
