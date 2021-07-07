from flask import session
import sqlite3
import os
import shutil
from function import user_function

# Find Object by searchType
def find_Object(searchType):
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    if searchType == 'All Types':
        if session.get('username'):
            fullList = curr.execute("SELECT * FROM object where uploader != '" + session['username'] + "'")
        else:
            fullList = curr.execute("SELECT * FROM object")
    else:
        if session.get('username'):
            fullList = curr.execute("SELECT * FROM object WHERE type = ? and (bidStatus = 0 or bidStatus = 1) and uploader != '?'", (searchType,session['username'],))
        else:
            fullList = curr.execute("SELECT * FROM object WHERE type = ? and (bidStatus = 0 or bidStatus = 1)", (searchType,))

    object_list = get_Object_Info(fullList)

    conn.close()

    return object_list;

# Find Object by accID
def get_Object(objectID):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()

    fullList = curr.execute("SELECT * FROM object WHERE objectID = ?", (objectID,))

    object_list = get_Object_Info(fullList)

    print("Hello ", object_list)

    conn.close()
    final = []
    for b in object_list:
    	final = b

    return final

# Find Object by accID
def get_Bid_Object(num):

    username = session['username']
    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()

    fullList = curr.execute("SELECT * FROM object WHERE bidderID = ? and bidStatus = ?", (username,num,))

    object_list = get_Object_Info(fullList)

    conn.close()

    return object_list

def get_Object_Info(fullList):
    object_list = []

    for a in fullList:
        asd = []
        count = 0
        for b in a:
            if type(b) is str and count != 3:
                asd.append(b.capitalize())
            else:
                asd.append(b)
            count += 1

        fullPath = '../../static/images/object/' + str(a[0]) + '/'
        mainImage = fullPath + 'main.png'
        sideImage1 = fullPath + 'side1.png'
        object_list.append(asd + [mainImage, sideImage1])

    return object_list

# Bid object
def bid_Object(objectID, bid):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()

    curr.execute("update object set currentPrice = ?, bidderID = ?, bidStatus = 1 where objectID = ?", (bid, session['username'],objectID,))

    conn.commit()
    conn.close()
    return True

# Buy Now object
def buy_Object(objectID, bid):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()

    curr.execute("update object set currentPrice = ?, bidderID = ?, bidStatus = 2 where objectID = ?", (bid, session['username'], objectID,))

    conn.commit()
    conn.close()
    return True

# Find Personal Object
def find_MyObject(username):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    object_list = []

    fullList = curr.execute("SELECT * FROM object WHERE uploader = ? and (bidStatus = 0 or bidStatus = 1)", (username,))

    object_list = get_Object_Info(fullList)

    conn.close()

    return object_list

# Find Personal Object
def find_MySoldObject(username):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    object_list = []

    fullList = curr.execute("SELECT * FROM object WHERE uploader = ? and bidStatus = 2", (username,))
    object_list = get_Object_Info(fullList)

    conn.close()

    return object_list


# Add Object
def add_Object(uploader, address, description, minimumPrice, buyNowPrice, objectType):
	conn = sqlite3.connect('data/main_data.db')
	insertStatement = 'INSERT INTO object(uploader,address,description,startingPrice,bidderID,currentPrice,buyNowPrice,type,bidStatus) VALUES(?,?,?,?,?,?,?,?,?)'
	data = [(uploader, address.lower(), description, minimumPrice, 0, 0,buyNowPrice, objectType,0)]
	conn.executemany(insertStatement, data)
	conn.commit()

	curr = conn.cursor()
	vals = curr.execute("SELECT objectID FROM object WHERE uploader=? and description=?", (uploader, description,))
	userID = 0
	for a in vals:
		userID = a[0]
	conn.close()

	return userID

# Delete Objcet
def remove_Object(objectID):
    conn = sqlite3.connect('data/main_data.db')
    conn.execute("delete from object where objectID = " + objectID)
    conn.commit()
    conn.close()

    path = 'static/images/object/' + str(objectID)
    shutil.rmtree(path)

    return True


def get_Object_Image(objectID):

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()
    imageList = ''

    fullList = curr.execute("SELECT * FROM object WHERE objectID = ?", (objectID,))
    for a in fullList:
        imageList = 'static/images/object/' + str(objectID) + '/main.png' 
    conn.close()

    return imageList

# Update accomodation address
def update_Object_Address(objectID, address):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update object set address = ? where objectID = ?"
    conn.execute(upAccomodation, (address, objectID))
    conn.commit()
    conn.close()
    return True

# Update accomodation description
def update_Object_Description(objectID, description):
    conn = sqlite3.connect("data/main_data.db")
    upAccomodation = "update object set description = ? where objectID = ?"
    conn.execute(upAccomodation, (description, objectID,))
    conn.commit()
    conn.close()
    return True