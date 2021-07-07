from flask import session
import sqlite3
import datetime

# Add booking
def add_Booking(userID, accID):
    conn = sqlite3.connect('data/main_data.db')
    insertStatement = "INSERT INTO booking(userID, accID) VALUES(?,?)"
    data = [(userID, accID)]
    conn.executemany(insertStatement, data)
    curr = conn.cursor()
    vals = curr.execute("SELECT bookingID FROM booking WHERE accID=?", (accID))
    bookingID = 0
    for a in vals:
        bookingID = a
    conn.commit()
    conn.close()
    return True

# Remove Booking
def remove_Booking(bookingID):
    conn = sqlite3.connect('data/main_data.db')
    booking1 = '"' + bookingID + '"'
    conn.execute("delete from user where bookingID = %s" % booking1)
    conn.commit()
    conn.close()
    return True

# check Booking -------- Not completed which need to know the things which should be showed
def check_Booking(userID):
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    # select
    vals = curr.execute("SELECT ?", )
    conn.commit()
    conn.close()
    return True

def update_Booking():
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()

    now = datetime.datetime.now()
    date = str(now.strftime("%Y-%m-%d"))

    curr.execute("update bookingTable set confirmed = 4 where endDate < " + date)

    conn.commit()
    conn.close()
    return