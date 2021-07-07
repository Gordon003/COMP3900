from flask import session
import sqlite3


def search_accomodation(location, eventList):
	#Search on keywords for location and event
	results = []
	region = sqlite3.connect('data/sydney_region.db')
	c2 = region.cursor()

	event_location = []

	north_sydney = 0
	north_sydney_list = []
	west_sydney = 0
	west_sydney_list = []
	south_sydney = 0
	south_sydney_list = []
	central_sydney = 0
	central_sydney_list = []

	best_region = ''

	# Get Central sydney
	fullList = c2.execute("select * from central_sydney")
	for town in fullList:
		central_sydney_list.append(town[0])

	# Get North sydney
	fullList = c2.execute("select * from north_sydney")
	for town in fullList:
		north_sydney_list.append(town[0])

	# Get South sydney
	fullList = c2.execute("select * from south_sydney")
	for town in fullList:
		south_sydney_list.append(town[0])

	# Get West sydney
	fullList = c2.execute("select * from west_sydney")
	for town in fullList:
		west_sydney_list.append(town[0])

	# Find Location
	# Location
	if location != "none":
		if location in central_sydney_list:
			best_region = 'Central'
		elif location in north_sydney_list:
			best_region = 'North'
		elif location in south_sydney_list:
			best_region = 'South'
		elif location in west_sydney_list:
			best_region = 'West'

	# Event List
	else:
		# Get event at location
		for place in central_sydney_list:
			if eventList.find(place) != -1:
				central_sydney += 1

		for place in north_sydney_list:
			if eventList.find(place) != -1:
				north_sydney += 1

		for place in south_sydney_list:
			if eventList.find(place) != -1:
				south_sydney += 1

		for place in west_sydney_list:
			if eventList.find(place) != -1:
				west_sydney += 1

		# Find highest location
		count = [central_sydney, north_sydney, south_sydney, west_sydney]
		best_count = max(count)

		if best_count == 0:
			best_region = 'All'
		elif central_sydney == best_count:
			best_region = 'Central'
		elif north_sydney == best_count:
			best_region = 'North'
		elif south_sydney == best_count:
			best_region = 'South'
		elif west_sydney == best_count:
			best_region = 'West'

	region.close()

	# Find accomodation
	main = sqlite3.connect('data/main_data.db')
	c2 = main.cursor()
	condition = ""
	count = 0
	best_region_list = []

	if best_region == "Central":
		best_region_list = central_sydney_list
	elif best_region == "North":
		best_region_list = north_sydney_list
	elif best_region == "South":
		best_region_list = south_sydney_list
	elif best_region == "West":
		best_region_list = west_sydney_list


	for location in best_region_list:
		if count == len(best_region_list) - 1:
			condition = condition + "'" + location + "'"
		else:
			condition = condition + "'" + location + "', "
		count += 1

	if session.get('username'):
		fullList = c2.execute("select * from accomodation where address in (" + condition + ") and uploader != '" + session['username'] + "'")
	else:
		fullList = c2.execute("select * from accomodation where address in (" + condition + ")")

	if best_region == 'All':
		if session.get('username'):
			fullList = c2.execute("select * from accomodation where uploader != '" + session['username'] + "'")
		else:
			fullList = c2.execute("select * from accomodation")

	accomodation_list = []
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

	main.close()
	return accomodation_list