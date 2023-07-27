import hashlib
import mysql.connector
mydb = mysql.connector.connect(host='localhost', user='root', password='yash', database='bms')


def open_acc():
    n = input('Enter your name')
    ac_no = input('Enter your account number')
    dob = input('Enter your birthdate')
    add = input('Enter the address')
    phn = input('Enter the contact number')
    opening_bal = int(input('Enter the amt to start with'))
    passkey = input('Enter your desired 4 digit key')
    hash = hashlib.sha1(passkey.encode())
    d1 = (ac_no, n, dob, add, phn, opening_bal, hash.hexdigest())
    d2 = (ac_no, n, opening_bal)
    sql1 = ('insert into account values(%s,%s,%s,%s,%s,%s,%s)')
    sql2 = ('insert into ledger values(%s,%s,%s)')
    x = mydb.cursor()
    x.execute(sql1,d1)
    x.execute(sql2,d2)
    mydb.commit()
    print('Account created successfully')
    main()


def auth():
    acc = input('Enter valid acc no')
    x = input('Enter the valid password')
    hash = hashlib.sha1(x.encode())
    d1 = (acc,)
    sql1 = ('select hashpass from account where accno = %s')
    mycursor = mydb.cursor()
    mycursor.execute(sql1, d1)
    result = mycursor.fetchone()
    if result[0] != hash.hexdigest():
        print('Wrong PassWord')
        return False
    else:
        print('Successfully Authenticated')
        return True, acc


def depo_amt():
    res, acc = auth()
    if not res:
        return
    amount = int(input('Enter the amount to be deposited'))
    sql1 = ('select balance from ledger where accno = %s')
    d1 = (acc,)
    mycursor = mydb.cursor()
    mycursor.execute(sql1, d1)
    result = mycursor.fetchone()
    t = amount + result[0]
    # Updating the ledger.
    sql2 = ('update ledger set balance = %s where accno = %s')
    d2 = (t, acc)
    mycursor.execute(sql2, d2)
    mydb.commit()
    main()


def remove_mon():
    res, acc = auth()
    if not res:
        return
    amount = int(input('Enter the amount to be withdrawn'))
    sql1 = ('select balance from ledger where accno = %s')
    d1 = (acc,)
    mycursor = mydb.cursor()
    mycursor.execute(sql1, d1)
    result = mycursor.fetchone()
    t = result[0] - amount
    if t <= 0:
        print('Insufficient Balance')
        return
    # Updating the ledger.
    sql2 = ('update ledger set balance = %s where accno = %s')
    d2 = (t, acc)
    mycursor.execute(sql2, d2)
    mydb.commit()
    main()


def bal_enq():
    res, acc = auth()
    if not res:
        return
    sql1 = ('select balance from ledger where accno = %s')
    d1 = (acc,)
    mycursor = mydb.cursor()
    mycursor.execute(sql1,d1)
    result = mycursor.fetchone()
    print('The money left in your account is Rs' + str(result[0]))
    main()


def disp():
    res, acc = auth()
    if not res:
        return
    sql1 = ('select * from account where accno = %s')
    d1 = (acc,)
    mycursor = mydb.cursor()
    mycursor.execute(sql1, d1)
    result = mycursor.fetchone()
    for i in result:
        print(i, end=" ")
    main()


def close_acc():
    res, acc = auth()
    if not res:
        return
    print("We want a written declaration saying:- 'I want to close my account'")
    x = input('Enter the declaration:-')
    if x != 'I want to close my account':
        return
    else:
        sql1 = ('delete from ledger where accno = %s')
        sql2 = ('delete from account where accno = %s')
        d1 = (acc,)
        mycursor = mydb.cursor()
        mycursor.execute(sql1, d1)
        mycursor.execute(sql2, d1)
        print('The deletion of Bank Account has been successful!')
        mydb.commit()
        main()


def main():
    print('''
        1. Open a new account.
        2. Deposit money.
        3. Withdraw money.
        4. Balance Enquiry.
        5. Display Customer Details.
        6. Close an account.
    ''')
    choice = input('Enter the choice:-')
    if choice == '1':
        open_acc()
    elif choice == '2':
        depo_amt()
    elif choice == '3':
        remove_mon()
    elif choice == '4':
        bal_enq()
    elif choice == '5':
        disp()
    elif choice == '6':
        close_acc()
    else:
        print('Invalid input, pls try again.')
        main()


main()
