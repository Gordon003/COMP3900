from flask import session
import sqlite3
import os
import shutil
from function import search_accomodation, user_function

# Find Accomodation by location or eventList
def find_Accomodation(location, eventList):
    accomodation_list = search_accomodation.search_accomodation(location, eventList)
    return accomodation_list

# Find Accomodation by accID
def get_Accomodation(accID):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    accomodation_list = []

    fullList = curr.execute("SELECT * FROM accomodation WHERE accID = ?", (accID,))
    for a in fullList:
        fullPath = '../../static/images/accomodation/' + str(a[0]) + '/'
        mainImage = fullPath + 'main.png'
        sideImage1 = fullPath + 'side1.png'
        sideImage2 = fullPath + 'side2.png'
        sideImage3 = fullPath + 'side3.png'
        
        asd = []
        for b in a:
            if type(b) is str:
                asd.append(b.capitalize())
            else:
                asd.append(b)
        accomodation_list.append(asd + [mainImage, sideImage1, sideImage2, sideImage3])

    conn.close()
    final = ""
    for b in accomodation_list:
    	final = b

    return final

# Find Accomodation by username
def find_MyAccomodation(username):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    accomodation_list = []

    fullList = curr.execute("SELECT * FROM accomodation WHERE uploader = ?", (username,))
    for a in fullList:
        fullPath = '../../static/images/accomodation/' + str(a[0]) + '/'
        mainImage = fullPath + 'main.png'
        sideImage1 = fullPath + 'side1.png'
        sideImage2 = fullPath + 'side2.png'
        sideImage3 = fullPath + 'side3.png'

        asd = []
        for b in a:
            if type(b) is str:
                asd.append(b.capitalize())
            else:
                asd.append(b)
        accomodation_list.append(asd + [mainImage, sideImage1, sideImage2, sideImage3])

    conn.close()

    return accomodation_list


# Add accomodation
def add_Accomodation(uploader, address, bedroom, washroom, description, price, houseType):
	conn = sqlite3.connect('data/main_data.db')
	insertStatement = 'INSERT INTO accomodation(uploader,address,bedroom,washroom,description,price,type) VALUES(?,?,?,?,?,?,?)'
	data = [(uploader, address, bedroom, washroom, description, price, houseType)]
	conn.executemany(insertStatement, data)
	conn.commit()

	curr = conn.cursor()
	vals = curr.execute("SELECT accID FROM accomodation WHERE uploader=? and description=?", (uploader, description,))
	userID = 0
	for a in vals:
		userID = a[0]
	conn.close()

	return userID

# Delete Accomodation
def remove_Accomodation(accID):
    conn = sqlite3.connect('data/main_data.db')
    conn.execute("delete from accomodation where accID = " + accID)
    conn.commit()
    conn.close()

    path = 'static/images/accomodation/' + accID
    shutil.rmtree(path)

    return True

# Update accomodation address
def update_Acc_Address(accID, address):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update accomodation set address = ? where accID = ?"
    conn.execute(upAccomodation, (address, accID))
    conn.commit()
    conn.close()
    return True

# Update accomodation bedroom
def update_Acc_Bedroom(accID, bedroom):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update accomodation set bedroom = ? where accID = ?"
    conn.execute(upAccomodation, (bedroom, accID))
    conn.commit()
    conn.close()
    return True

# Update accomodation washroom
def update_Acc_Washroom(accID, washroom):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update accomodation set washroom = ? where accID = ?"
    conn.execute(upAccomodation, (washroom, accID))
    conn.commit()
    conn.close()
    return True

# Update accomodation description
def update_Acc_Description(accID, description):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update accomodation set description = ? where accID = ?"
    conn.execute(upAccomodation, (description, accID))
    conn.commit()
    conn.close()
    return True

# Update accomodation price
def update_Acc_Price(accID, price):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update accomodation set price = ? where accID = ?"
    conn.execute(upAccomodation, (price, accID))
    conn.commit()
    conn.close()
    return True

# Update accomodation type
def update_Acc_Type(type):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update accomodation set type = ? where accID = ?"
    conn.execute(upAccomodation, (type, accID))
    conn.commit()
    conn.close()
    return True

# Update accomodation main image
def update_Acc_Main_image(main_image):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update accomodation set main_image = ? where accID = ?"
    conn.execute(upAccomodation, (main_image, accID))
    conn.commit()
    conn.close()
    return True

def add_Booking(accID, start_Date, end_Date, number_of_day):
    # Get accomodation
    accom = get_Accomodation(accID)
    ownerID = user_function.get_UserID_name(accom[1])
    price = accom[6]

    conn = sqlite3.connect("data/main_data.db")
    insertStatement = 'INSERT INTO bookingTable(accomID, buyerID, sellerID, startDate, endDate, price, day, confirmed) VALUES(?,?,?,?,?,?,?, ?)'
    data = [(accID, session['accID'], ownerID, start_Date, end_Date, price, number_of_day, 0)]
    conn.executemany(insertStatement, data)
    conn.commit()
    conn.close()

    # Get money
    user_function.remove_money(price * number_of_day)

    return True

# Delete Accomodation
def remove_Booking(bookingID):
    conn = sqlite3.connect('data/main_data.db')
    conn.execute("delete from bookingTable where id = " + bookingID)
    conn.commit()
    conn.close()

    return True

# Find booking that required a response from other people
def find_myWaitBooking(userID):

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM bookingTable WHERE buyerID =? and confirmed = 0", (userID,))

    bookingList = []
    for a in vals:
        bookingList.append(a + (get_Accomodation_Image(a[1]), user_function.get_Username(a[3])))
    conn.close()

    return bookingList

# Find booking that has been confirmed
def find_myConfirmedBooking(userID):

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM bookingTable WHERE buyerID =? and confirmed = 1", (userID,))

    bookingList = []
    for a in vals:
        bookingList.append(a + (get_Accomodation_Image(a[1]), user_function.get_Username(a[3])))
    conn.close()

    return bookingList

# Find booking from other people to your accomodation and need your confirmation
def find_otherPeopleBooking(userID):

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM bookingTable WHERE sellerID =? and confirmed = 0", (userID,))

    bookingList = []
    for a in vals:
        buyerName = user_function.get_Username(a[2])
        bookingList.append(a + (buyerName,get_Accomodation_Image(a[1]),))
    conn.close()

    return bookingList

# Find booking from other people to your accomodation and is confirmed
def find_otherPeopleConfirmedBooking(userID):

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM bookingTable WHERE sellerID =? and confirmed = 1", (userID,))

    bookingList = []
    for a in vals:
        buyerName = user_function.get_Username(a[2])
        bookingList.append(a + (buyerName,get_Accomodation_Image(a[1]),))
    conn.close()

    return bookingList

# Find booking from other people to your accomodation and is confirmed via accountID
def find_otherPeopleConfirmedBooking2(accID):

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM bookingTable WHERE accomID =? and confirmed = 1", (accID,))

    bookingList = []
    for a in vals:
        buyerName = user_function.get_Username(a[2])
        bookingList.append(a + (buyerName,get_Accomodation_Image(a[1]),))
    conn.close()

    return bookingList

# Find rejected booking
def find_myRejectedBooking():

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("SELECT * FROM bookingTable WHERE buyerID =? and confirmed = -1", (session['accID'],))

    bookingList = []
    for a in vals:
        buyerName = user_function.get_Username(a[2])
        bookingList.append(a + (buyerName,get_Accomodation_Image(a[1]),))
    conn.close()

    return bookingList

# Accept booking
def accept_Booking(bookingID):

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("update bookingTable set confirmed = 1 where id =?", (bookingID,))
    conn.commit()
    return True

# Reject booking
def reject_Booking(bookingID):

    conn = sqlite3.connect("data/main_data.db")
    curr = conn.cursor()
    vals = curr.execute("update bookingTable set confirmed = -1 where id =?", (bookingID,))
    conn.commit()

    bookingList = curr.execute("select * from bookingTable where id =?", (bookingID,))
    book = ""
    for n in bookingList:
        book = n

    conn.close()

    user_function.add_Money_To_Other_User(book[2], book[6] * book[7])
    return True

# Get main image of accomodation
# Find Accomodation by username
def get_Accomodation_Image(accID):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    imageList = ''

    fullList = curr.execute("SELECT * FROM accomodation WHERE accID = ?", (accID,))
    for a in fullList:
        imageList = '../../static/images/accomodation/' + str(accID) + '/main.png' 
    conn.close()

    return imageList

def find_date_difference(start_date, end_date):
    start = start_date[8] + start_date[9]
    start = int(start)

    end = end_date[8] + end_date[9]
    end = int(end)

    return end - start

def get_Accom_Availability(accID):

    finalBooking = [0] * 31

    accomodation = get_Accomodation(accID)
    confirmedBooking = find_otherPeopleConfirmedBooking2(accID)

    for booking in confirmedBooking:
        start_Date = int(booking[4][-2:])
        end_Date = int(booking[5][-2:])

        while(start_Date != end_Date + 1):
            finalBooking[start_Date] = 1
            start_Date += 1

    return finalBooking

def check_Booking_Inbetween(start_Date, end_Date, booking):

    start = int(start_Date[-2:])
    end = int(end_Date[-2:])

    while (start != end + 1):
        if booking[start] == 1:
            return False
        start += 1

    return True