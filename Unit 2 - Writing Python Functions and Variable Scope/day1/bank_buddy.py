# Prints the welcome message
# Parameters: none
# Returns: nothing
def start_bank_session():
    print("🏦 Welcome to Bank Buddy!")

# Calculates new balance after deposit
# Parameters: balance (float), deposit (float)
# Returns: updated balance (float)
def deposit_money(balance, deposit):
    return balance + deposit

# Calculates new balance after withdrawal
# Parameters: balance (float), withdrawal (float)
# Returns: updated balance (float)
def withdraw_money(balance, withdrawal):
    return balance - withdrawal

# Prints a transaction summary
# Parameters: name (string), balance (float)
# Returns: nothing
def show_summary(name, balance):
    print(name + "'s current balance is $" + str(round(balance, 2)))



# 1. Call start_bank_session().
# 2. Store "Aiden" in a variable called name.
# 3. Store 100.00 in a variable called balance.
# 4. Deposit 25.50 using deposit_money() and update balance.
# 5. Withdraw 40.00 using withdraw_money() and update balance.
# 6. Call show_summary(name, balance) to print the final amount.

start_bank_session()
name = "Aiden"
balance = 100.00
balance = deposit_money(balance, 25.50)
balance = withdraw_money(balance, 40.00)
show_summary(name, balance) 