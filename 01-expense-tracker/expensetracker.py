import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"
print("CSV path →", os.path.abspath("expenses.csv"))

def add_expense():
    category = input("Enter category (Food/Travel/Other): ").strip() 
    amount = input("Enter amount: ").strip()
    note = input("Add a note (optional): ").strip()
    if note == "":
        note = "No note" #when note left blank
    date = input("Enter date (leave blank for today):").strip()
    if date == "": # to add other dates expenses
        date = datetime.now().strftime("%d/%m/%y") #present date expense
    else:
        try:
            datetime.strptime(date, "%d%m/%y")
        except ValueError:
            print("Invalid date format. Please use DD/MM/YYYY")
            return
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, mode='a', newline='') as file: #opens file and appends data in a new line
        writer = csv.writer(file) #prepares to write to CSV
        if not file_exists or os.stat(FILE_NAME).st_size == 0:
            writer.writerow(["Date","Category","Amount","Note"])
        writer.writerow([date, category, amount, note])#writes data into file
    print("✅ Expense added successfully!")

def view_expenses():
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            rows = [row for row in reader if row]  # Skip blank lines

            if len(rows) <= 1:
                print("No expenses found yet!")
                return

            header = rows[0]
            data_rows = rows[1:]

            try:
                # Strip spaces and handle potential bad rows
                cleaned_rows = []
                for row in data_rows:
                    if len(row) < 4:
                        continue  # Skip bad/incomplete rows
                    date_str = row[0].strip()
                    # Parse date
                    parsed_date = datetime.strptime(date_str, "%d/%m/%Y")
                    cleaned_rows.append((parsed_date, row))

                # Sort based on parsed date
                cleaned_rows.sort(key=lambda x: x[0])
                sorted_rows = [row for _, row in cleaned_rows]

            except Exception as e:
                print("❌ Error in sorting. Please check date format in CSV.")
                return

            # Print header
            print("\n📄 Your Expenses:")
            print("{:<12} {:<15} {:<10} {}".format("Date", "Category", "Amount", "Note"))
            print("-" * 50)

            for row in sorted_rows:
                print(f"{row[0]:15} | {row[1]:10} | {row[2]:7} | {row[3]}")

    except FileNotFoundError:
        print("No expenses recorded yet.")


def total_spent():
    total = 0 #variable to keep track of sum
    try:
        with open(FILE_NAME, mode='r') as file: #opens csv file in read mode
            reader = csv.reader(file) #creates csv reader
            next(reader, None)  # Skips the header

            for row in reader:
                try:
                    total += float(row[2])
                except:
                    continue
        print(f"\n💰 Total Spent: ₹{total:.2f}")
    except FileNotFoundError:
        print("No expenses found.")

def main():
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Spent")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            total_spent()
        elif choice == '4':
            print("👋 Exiting... Have a thrifty day!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
