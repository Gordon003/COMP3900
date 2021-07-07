from flask import Flask, render_template, request, session, redirect, url_for, Blueprint
from function import data_function, user_function, sort, accom_function
from user import user
from accom import accom
from objects import objects
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(user)
app.register_blueprint(accom)
app.register_blueprint(objects)

# HOME PAGE
@app.route('/')
def index():
	return render_template('home/home.html', user = user_function.group_User_Info())

# ACCOMODATION SEARCH HOME PAGE
@app.route('/accomodation', methods = ["GET", "POST"])
def accomodation():
	# POST Method
	if request.method == "POST":
		searchLocation = request.form['location']
		eventList = [0] * 3

		if not searchLocation:
			searchLocation = "None"
		eventList[0] = request.form['event1']
		if not eventList[0]:
			eventList[0] = "null"	
		eventList[1] = request.form['event2']
		if not eventList[1]:
			eventList[1] = "null"	
		eventList[2] = request.form['event3']
		if not eventList[2]:
			eventList[2] = "null"	
		return redirect(url_for('accom.accomodation_result', location = searchLocation, eventList = eventList))
	# GET Method
	else:
		central_sydney_event_list, north_sydney_event_list, west_sydney_event_list, south_sydney_event_list = data_function.get_Event();
		return render_template('accomodation/home_accomodation.html', user = user_function.group_User_Info(), central_sydney_event_list = central_sydney_event_list, north_sydney_event_list = north_sydney_event_list, west_sydney_event_list = west_sydney_event_list, south_sydney_event_list = south_sydney_event_list)

# OBJECT SEARCH HOME PAGE
@app.route('/object', methods = ["GET", "POST"])
def object():
	# POST Method
	if request.method == "POST":
		searchType = request.form['searchType']
		if searchType == "":
			searchType = 'null'
		searchType = searchType.lower()
		return redirect(url_for('objects.object_result', searchType = searchType))
	# GET Method
	else:
		object_list = data_function.get_Object()
		return render_template('object/home_object.html', user = user_function.group_User_Info(), object_list = object_list)