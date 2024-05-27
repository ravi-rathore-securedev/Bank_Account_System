import sqlite3
import random
import string
from tabulate import tabulate

con=sqlite3.connect('Bank_system.db')

cursor=con.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS accounts (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   dob TEXT NOT NULL,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL,
                   account_number TEXT NOT NULL,
                   phone_number TEXT NOT NULL,
                   email TEXT NOT NULL,
                   address TEXT NOT NULL
               )
               ''')


cursor.execute('''
               CREATE TABLE IF NOT EXISTS transactions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   account_number TEXT NOT NULL,
                   Deposit REAL,
                   Withdraw REAL,
                   Balance REAL NOT NULL,
                   Operation TEXT NOT NULL,
                   FOREIGN KEY (account_number) REFERENCES accounts(account_number)
               )
               ''')

def Initial_operation():
    print('\n')
    print('******* Bank Management System *******')
    print('\n')
    print('1. New Account Opening')
    print('2. Account Login')
    print('3. Forgot username and Password')
    print("4. View All Account Holders Details")
    print('5. Exit the Bank Operation')

def Transactional_operation():
    print('\n')
    print('******* Perform Transaction *******')
    print('\n')
    print('1. View Balance')
    print('2. Deposit Amount')
    print('3. Withdraw Amount')
    print('4. Transfer Amount')
    print('5. View Transaction History')
    print('6. View User Details')
    print('7. Update User Details')
    print('8. Delete User Details')
    print('9. Exit the Transaction')

def New_Account():
        print('\n')
        name=input('Enter your Full Name: ')
        name=name.strip()
        dob=input('Enter your date of birth(DD/MM/YYYY): ')
        phone_Number=input('Enter your phone number: ')
        email=input('Enter your email address: ')
        address=input('Enter your current address: ')
        password=input('Enter the secure password: ')
        username=name[0:4] + dob[6:10]
        account_number=int(random.random()*10**12)
        
        cursor.execute('INSERT INTO accounts (name, dob, username, password, account_number, phone_number, email, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name, dob, username, password, account_number, phone_Number, email, address))
        
        con.commit()
        
        print('\n \t\t\t\t\t\t\t\t\t\t Your Account is created Successfully')
        print(f'\n Your Account Number is {account_number} \n Username is {username} \n password is {password}')


def Account_login():
    print('\n\t\t\t\t\t\t\t\t ****** Provide Login Credentials ****** \n')
    verify_username=input('Enter your username: ')
    verify_password=input('Enter your password: ')
    
    cursor.execute('SELECT account_number FROM accounts WHERE username = ? AND password = ?', (verify_username, verify_password))
    
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            transactionAccNumber=row[0]

    else:
        print('\n \t\t\t\t\t\t\t\t\t\t Invalid username or password.')
        return
        
        
    def Total_Balance():
        cursor.execute('SELECT Balance FROM transactions WHERE account_number = ? ORDER BY id DESC LIMIT 1', (transactionAccNumber,))
        balance_row = cursor.fetchone()

        if balance_row is not None:
            total_balance = balance_row[0]
            return total_balance
        else:
            return 0
        
    def Balance():
        acc_balance=Total_Balance()
        print(f'\n \t\t\t\t\t\t\t\t\t\t Available Account Balance: Rs.{acc_balance}')
        

    def Amount_Deposit():
        print('\n')
        deposit=input('Enter the amount to deposit in the account in Rs: ')
        current_balance=Total_Balance()
        new_Balance=int(current_balance)+int(deposit)
        
        cursor.execute('INSERT INTO transactions (account_number, Deposit, Balance, Operation) VALUES (?, ?, ?, ?)',(transactionAccNumber,deposit,new_Balance, 'Deposit'))
        con.commit()
        print(f'\n \t\t\t\t\t\t\t\t\t\t {deposit} Deposited Successfully \n')

    def Amount_Withdraw():
        print('\n')
        withdraw=input('Enter the amount to withdraw from the account in Rs: ')
        current_balance=Total_Balance()
        if(current_balance>=int(withdraw)):
            new_balance=int(current_balance)-int(withdraw)
            
            cursor.execute('INSERT INTO transactions (account_number, Withdraw, Balance, Operation) VALUES (?, ?, ?, ?)',(transactionAccNumber,withdraw,new_balance, 'Withdraw'))
            con.commit()
            
            print(f'\n \t\t\t\t\t\t\t\t\t\t {withdraw} Withdrawn Successfully \n')
        else:
            print('\n \t\t\t\t\t\t\t\t\t\t Not enough Balance to perform transaction')
    

    def Amount_Transfer():
        print('\n')
        transfer_acc=input('Enter the account number to transfer to: ')
        transfer_amount=input('Enter the amount to transfer in Rs: ')
        current_balance=Total_Balance()
        if(current_balance>=int(transfer_amount)):
            new_balance=int(current_balance)-int(transfer_amount)
            
            cursor.execute('INSERT INTO transactions (account_number, Withdraw, Balance, Operation) VALUES (?, ?, ?, ?)', (transactionAccNumber,transfer_amount, new_balance, f'Transfer to {transfer_acc}'))
            
            cursor.execute('SELECT Balance FROM transactions WHERE account_number = ? ORDER BY id DESC LIMIT 1', (transfer_acc,))
            receiver_balance_row=cursor.fetchone()
            
            receiver_balance=receiver_balance_row[0] if receiver_balance_row else 0
            
            new_receiver_balance=int(receiver_balance)+int(transfer_amount)
            
            cursor.execute('INSERT INTO transactions (account_number, Deposit, Balance, Operation) VALUES (?, ?, ?, ?)',(transfer_acc,transfer_amount,new_receiver_balance,f'Transfer from {transactionAccNumber}'))
            con.commit()
            
            characters = string.ascii_letters + string.digits
            username=''.join(random.choice(characters) for _ in range(8))
            
            password=int(random.random()*10**4)
            
            cursor.execute('INSERT INTO accounts (name,dob,username,password,account_number, phone_number, email, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',('user','01/01/2001',username,password,transfer_acc, '00001','email','city'))
            con.commit()
            
            print(f'\n  \t\t\t\t\t\t\t\t\t\t {transfer_amount} transferred Successfully to account {transfer_acc}')
        else:
            print('\n \t\t\t\t\t\t\t\t\t\t  Not Enough Balance to transfer Amount. \n')
        
    def Transaction_history():
        print('\n Account Transactions History \n')
        cursor.execute('SELECT * FROM transactions WHERE account_number=? ',(transactionAccNumber,))
        rows=cursor.fetchall()
        headers=['ID','Account Number', 'Deposit Amount(Rs)', 'Withdrawal Amount(Rs)', 'Available Balance(Rs)', 'Operation Performed' ]
        
        table_data=[(row[0],row[1],row[2],row[3],row[4],row[5]) for row in rows]
        
        print(tabulate(table_data, headers, tablefmt='grid'))
    
    
    def User_details():
        print('\n')
        cursor.execute('SELECT * FROM accounts WHERE account_number=?',(transactionAccNumber,))
        rows=cursor.fetchall()
        
        headers = [ 'Name', 'DOB', 'Account Number', 'Phone Number', 'Email ID', 'Address']
        
        table_data = [(row[1], row[2],row[5], row[6], row[7], row[8]) for row in rows]
        
        print(tabulate(table_data, headers, tablefmt='grid'))
        
    def Update_user():
        print('\n')
        name=input('Enter your Full Name: ')
        name=name.strip()
        dob=input('Enter your date of birth(DD/MM/YYYY): ')
        phone_Number=input('Enter your phone number: ')
        email=input('Enter your email address: ')
        address=input('Enter your current address: ')
        username=input('Enter the preferred username: ')
        password=input('Enter the secure password: ')
        
        cursor.execute('UPDATE accounts SET name=?, dob=?, phone_number=?, email=?, address=?, username=?, password=? WHERE account_number=?',(name,dob,phone_Number,email,address,username,password,transactionAccNumber))
        con.commit()
        print('\n \t\t\t\t\t\t\t\t\t\t User Details Updated Successfully')
    
    def Delete_user():
        cursor.execute('DELETE FROM accounts WHERE account_number=?',(transactionAccNumber,))
        con.commit()
        print('\n User Data Deleted Successfully')
    
    
    while(True):
        Transactional_operation()
        print('\n')
        choice=input('Enter your choice to perform Account transaction: ')
        
        match choice:
            case '1':
                Balance()
            case '2':
                Amount_Deposit()
            case '3':
                Amount_Withdraw()
            case '4':
                Amount_Transfer()
            case '5':
                Transaction_history()
            case '6':
                User_details()
            case '7':
                Update_user()
            case '8':
                Delete_user()
            case '9':
                break
            case _:
                print('\n')
                print('***  INVALID CHOICE  ***')


def Reset_account():
    print('\n')
    acc_number=input('Enter your account number:')
    
    cursor.execute('SELECT username, password FROM accounts WHERE account_number=?',(acc_number,))
    
    rows=cursor.fetchall()
    if rows:
        for row in rows:
            print(f'\n Username: {row[0]} \t Password: {row[1]}')
    
    else:
        print('\n \t\t\t\t\t\t\t\t\t\t Invalid Account Number ')
    
def All_user_details():
    print('\n All Account Holder Details')
    cursor.execute('SELECT * FROM accounts')
    rows=cursor.fetchall()
    
    headers=['ID', 'Name', 'DOB','Username', 'Password', 'Account Number', 'Phone Number', 'Email ID', 'Address']
    
    table_data = [(row[0], row[1], row[2], row[3], row[4],  row[5], row[6], row[7], row[8]) for row in rows]
    
    print(tabulate(table_data, headers, tablefmt='grid'))


def main():
    while True:
        Initial_operation()
        print('\n')
        choice=input('Enter your choice to perform Account Operations: ')
        
        match choice:
            case '1':
                New_Account()
            case '2':
                Account_login()
            case '3':
                Reset_account()
            case '4':
                All_user_details()
            case '5':
                break
            case _:
                print('\n')
                print('***  INVALID CHOICE  ***')
        
    con.close()
    
if __name__=='__main__':
    main()