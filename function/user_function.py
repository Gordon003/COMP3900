from flask import session
from function import checker
import sqlite3
import re
import os

# Get User via username
def get_User(username):
    #Check from user database
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM user WHERE name=?", (username,))

    # Get user data
    user = []
    for a in vals:
        user = a[1:5]
        user += (0, str('../static/images/user/' + username + '.png'),)

    # Close connection
    conn.close()
    return user

#Find UserID by name
def get_Username(userID):
    #Check from user database
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    vals = curr.execute("SELECT name FROM user WHERE userID=?", (userID,))

    # Get user data
    user = 0
    for a in vals:
        user = a[0]

    # Close connection
    conn.close()
    return user

#Find UserID by name
def get_UserID_name(username):
    #Check from user database
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    vals = curr.execute("SELECT userID FROM user WHERE name=?", (username,))

    # Get user data
    user = 0
    for a in vals:
        user = a[0]

    # Close connection
    conn.close()
    return user

# Add user to database
def add_User(username, password, phone, address, email):
    # Add
    conn = sqlite3.connect('data/main_data.db')
    insertStatement = "INSERT INTO user(name,phone,address,email,balance,password) VALUES(?,?,?,?,?,?)"
    data = [(username, phone, address, email, 0, password)]

    # Get ID
    conn.executemany(insertStatement, data)
    curr = conn.cursor()
    vals = curr.execute("SELECT userID FROM user WHERE name=?", (username,))
    userID = 0
    for a in vals:
        userID = a
    conn.commit()
    conn.close()

    # Update Session
    session['accID'] = userID[0]
    session['logged_in'] = True
    session['username'] = username
    session['phone'] = phone
    session['address'] = address
    session['email'] = email
    session['balance'] = 0
    session['icon'] = '../static/images/user/' + username + '.png'
    session['password'] = password
    return True

# Remove user
def remove_User(userID):
    conn = sqlite3.connect('data/main_data.db')
    user1 = '"' + userID + '"'
    conn.execute("delete from user where userID = %s" % user1)
    conn.commit()
    conn.close()
    return True

# Update user name
def update_Username(username):
    if not checker.check_unique_name(username):
        return False

    oldUsername = session['username']
    conn = sqlite3.connect("data/main_data.db")
    upUser = "update user set name = ? where userID = ?"
    conn.execute(upUser, (username, session['accID']))
    conn.commit()
    conn.close()
    session['username'] = username

    return True

# Update user password
def update_Password(password1, password2):
    if password1 != password2 or password1 == session['password']:
        return False

    conn = sqlite3.connect("data/main_data.db")
    upUser = "update user set password = ? where userID = ?"
    conn.execute(upUser, (password1, session['accID']))
    conn.commit()
    conn.close()
    session['password'] = password1
    return True

# Update user phone
def update_Phone(phone):
    conn = sqlite3.connect("data/main_data.db")
    upUser = "update user set phone = ? where userID = ?"
    conn.execute(upUser, (phone, session['accID']))
    conn.commit()
    conn.close()
    session['phone'] = phone
    return True

# Update user address
def update_Address(address):
    conn = sqlite3.connect("data/main_data.db")
    upUser = "update user set address = ? where userID = ?"
    conn.execute(upUser, (address, session['accID']))
    conn.commit()
    conn.close()
    session['address'] = address
    return True

# Update user email
def update_Email(email):
    conn = sqlite3.connect("data/main_data.db")
    upUser = "update user set email = ? where userID = ?"
    conn.execute(upUser, (email, session['accID']))
    conn.commit()
    conn.close()
    session['email'] = email
    return True

def get_User_Balance(username):
    #Check from user database
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    vals = curr.execute("SELECT balance FROM user WHERE name=?", (username,))

    # Get user data
    balance = 0
    for a in vals:
        balance = a[0]

    # Close connection
    conn.close()
    return balance

# Group user info for HTML Jinja
def group_User_Info():
    if not session:
        return
    else:
        session['balance'] = get_User_Balance(session['username'])
        return [session['username'], session['phone'], session['address'].capitalize(), session['email'], session['balance'], session['icon']]

def add_money(amount):
    conn = sqlite3.connect("data/main_data.db")
    upUser = "update user set balance = balance + ? where userID = ?"
    conn.execute(upUser, (amount, session['accID']))
    conn.commit()

    session['balance'] = session['balance'] + int(amount)

    return True

def add_Money_To_Other_User(userID, amount):
    conn = sqlite3.connect("data/main_data.db")
    upUser = "update user set balance = balance + ? where userID = ?"
    conn.execute(upUser, (amount, userID))
    conn.commit()

    if session['accID'] == userID:
        session['balance'] += amount

    return True

def remove_money(amount):
    conn = sqlite3.connect("data/main_data.db")
    upUser = "select balance from user where userID = ?"
    upUser2 = "update user set balance = balance - ? where userID = ?"
    result = conn.execute(upUser, (session['accID'],))

    balance = 0
    for a in result:
        balance = a[0]
    if balance < int(amount):
        conn.close()
        return False
    else:
        session['balance'] -= int(amount)
        conn.execute(upUser2, (amount, session['accID']))
        conn.commit()
        conn.close()
        return True