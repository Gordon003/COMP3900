from flask import session
import sqlite3
import re

# Check user
def check_Correct_User(username, password):

    # Check from database
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM user WHERE name=? and password = ?", (username, password))
    user = []
    for a in vals:
        user = a
    conn.close()

    # No user - false
    if not user:
        return False

    # Update Session - true
    session['accID'] = user[0]
    session['username'] = user[1]
    session['phone'] = user[2]
    session['address'] = user[3]
    session['email'] = user[4]
    session['balance'] = user[5]
    session['icon'] = '../static/images/user/' + user[1] + '.png'
    session['password'] = user[6]
    return True

# Check user name is unique or not
def check_unique_name(username):

    if username == '':
        return False

    # Find username in database
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM user WHERE name=?", (username,))
    user = []
    for a in vals:
        user = a
    conn.close()

    if not user:
        return True
    else:
        return False

# Check valid password
def check_valid_password(password):
    if len(password) < 6:
        return False
    else:
        return True

# Check valid phone number
def check_valid_phone(phone):
    if not phone.isdigit() or not len(phone) == 10:
        return False
    else:
        return True

# Check valid price
def check_valid_price(price):
    price = re.sub('[!@#$]', '', price)
    if not price.isdigit():
        return False
    else:
        return True

# Check valid address
def check_valid_address(address):
    city = address.lower()

    conn = sqlite3.connect('data/sydney_region.db')
    curr = conn.cursor()

    # Central Sydney
    vals = curr.execute("SELECT * FROM central_sydney WHERE name=?", (city,))
    for a in vals:
        conn.close()
        return True

    # North Sydney
    vals = curr.execute("SELECT * FROM north_sydney WHERE name=?", (city,))
    for a in vals:
        conn.close()
        return True

    # South Sydney
    vals = curr.execute("SELECT * FROM south_sydney WHERE name=?", (city,))
    for a in vals:
        conn.close()
        return True

    # West Sydney
    vals = curr.execute("SELECT * FROM west_sydney WHERE name=?", (city,))
    for a in vals:
        conn.close()
        return True

    conn.close()
    return False

# Check valid email
def check_valid_email(email): 
    if re.match(r'^.*[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[0-9a-zA-Z]{1,3}.*$', email): 
        return True
    else:
        return False
