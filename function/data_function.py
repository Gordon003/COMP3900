from flask import session
import sqlite3

accom_image_directory = '../static/images/accomodation/'

# Retrieve Event database
def get_Event():

    conn = sqlite3.connect('data/main_data.db')
    curr = conn.cursor()

    central_sydney_event_list = []
    north_sydney_event_list = []
    west_sydney_event_list = []
    south_sydney_event_list = []

    # Central Sydney
    fullList = curr.execute("SELECT * FROM event where region = 'central'")
    for a in fullList:
    	b = [a[0], a[1].capitalize(), a[2]]
    	central_sydney_event_list.append(b)

    # North Sydney
    fullList = curr.execute("SELECT * FROM event where region = 'north'")
    for a in fullList:
    	b = [a[0], a[1].capitalize(), a[2]]
    	north_sydney_event_list.append(b)

    # West Sydney
    fullList = curr.execute("SELECT * FROM event where region = 'west'")
    for a in fullList:
    	b = [a[0], a[1].capitalize(), a[2]]
    	west_sydney_event_list.append(b)

    # South Sydney
    fullList = curr.execute("SELECT * FROM event where region = 'south'")
    for a in fullList:
    	b = [a[0], a[1].capitalize(), a[2]]
    	south_sydney_event_list.append(b)

    conn.close()
    return central_sydney_event_list, north_sydney_event_list, west_sydney_event_list, south_sydney_event_list

# Get Object Type
def get_Object():

	conn = sqlite3.connect('data/main_data.db')
	curr = conn.cursor()
	object_list = []

	fullList = curr.execute("SELECT * FROM accepted_object")

	for a in fullList:
		cap = a[0].capitalize()
		object_list.append(cap)

	conn.close()
	return object_list
