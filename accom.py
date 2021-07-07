from flask import Flask, render_template, request, session, redirect, url_for, Blueprint
from function import data_function, user_function, sort, accom_function, complaint
import os

accom = Blueprint('accom', __name__)

# ACCOMODATION RESULT PAGE
@accom.route('/accomodation/search+<location>+<eventList>', methods = ["GET", "POST"])
def accomodation_result(location, eventList):
	# Get accomodation list
	accomodation_list = accom_function.find_Accomodation(location.lower(), eventList.lower())

	# POST Method
	if request.method == "POST":
		editInfo = request.form['submit']
		# Sort by address
		if editInfo == 'location':
			accomodation_list = sort.sort_Accomodation_List(accomodation_list,2)
		# Sort by price Lowest -> Highest
		elif editInfo == 'priceLH':
			accomodation_list = sort.sort_Accomodation_List(accomodation_list,6, False)
		# Sort by price Highest -> Lowest
		elif editInfo == 'priceHL':
			accomodation_list = sort.sort_Accomodation_List(accomodation_list,6, True)
		# Only get house or mansion or apartment
		elif editInfo == 'House' or editInfo == 'Apartment' or editInfo == 'Mansion':
			accomodation_list = sort.get_Accomodation_Type(accomodation_list, editInfo)

	# GET Method
	return render_template('accomodation/search.html', user = user_function.group_User_Info(), objectList = accomodation_list)

# ACCOMODATION VIEW PAGE
@accom.route('/accomodation/<accID>', methods = ["GET", "POST"])
def accomodation_view(accID):
	accomodation = accom_function.get_Accomodation(accID)
	if accomodation != "":
		return render_template('accomodation/accomodation_view.html', user = user_function.group_User_Info(), accomodation = accomodation)
	else:
		return "None"

# ACCOMODATION REPORT PAGE
@accom.route('/accomodation/<accID>/report', methods = ["GET", "POST"])
def accomodation_report(accID):
	accomodation = accom_function.get_Accomodation(accID)

	if request.method == 'POST':
		complaint_info = request.form['complaint']
		if complaint_info != "":
			complaint.send_Complaint(accID, complaint_info, "accomodation")
			return render_template('accomodation/accomodation_report_confirm_notif.html', user = user_function.group_User_Info(), accomodation = accomodation)

	if accomodation != "":
		return render_template('accomodation/accomodation_report.html', user = user_function.group_User_Info(), accomodation = accomodation)
	else:
		return "None"

# ACCOMODATION BOOKING PAGE
@accom.route('/accomodation/<accID>/booking', methods = ["GET", "POST"])
def accomodation_booking(accID):

	accom = accom_function.get_Accomodation(accID)
	booking = accom_function.get_Accom_Availability(accID)

	if request.method == "POST":
		if request.form['button'] == 'back':
			return redirect(url_for('accom.accomodation_view', accID = accID))
		start_Date = request.form['start_Date']
		end_Date = request.form['end_Date']
		available_Booking = accom_function.check_Booking_Inbetween(start_Date, end_Date, booking)
		if start_Date and end_Date and end_Date >= start_Date and available_Booking:
			number_of_day = accom_function.find_date_difference(start_Date, end_Date)
			total_cost = number_of_day * accom[6]
			if total_cost <= session['balance']:
				return redirect(url_for('accom.accomodation_booking_confirm', accID = accID, start_Date = start_Date, end_Date = end_Date))
			else:
				error = 'error1'
				return render_template('accomodation/accomodation_booking.html', user = user_function.group_User_Info(), accomodation = accom, error = error, booking = booking)
		else:
			error = 'error2'
			return render_template('accomodation/accomodation_booking.html', user = user_function.group_User_Info(), accomodation = accom, error = error, booking = booking)

	return render_template('accomodation/accomodation_booking.html', user = user_function.group_User_Info(), accomodation = accom, booking = booking)

# ACCOMODATION CONFIRMATION
@accom.route('/accomodation/<accID>/booking/confirm/<start_Date>+<end_Date>', methods = ["GET", "POST"])
def accomodation_booking_confirm(accID, start_Date, end_Date):
	accom = accom_function.get_Accomodation(accID)
	number_of_day = accom_function.find_date_difference(start_Date, end_Date)
	total_cost = number_of_day * accom[6]

	if request.method == "POST":
		command = request.form['buttonHit']

		if command == 'confirm':
			accom_function.add_Booking(accID, start_Date, end_Date, number_of_day)
			return redirect(url_for('accom.accomodation_booking_enter', accID = accID, start_Date = start_Date, end_Date = end_Date))
		else:
			return redirect(url_for('accom.accomodation_booking', accID = accID))

	return render_template('accomodation/accomodation_booking_confirm.html', user = user_function.group_User_Info(), accID = accID, accomodation = accom, start = start_Date, end = end_Date, cost = total_cost)

# ADD BOOKING
@accom.route('/accomodation/<accID>/booking/confirm/<start_Date>+<end_Date>/enter')
def accomodation_booking_enter(accID, start_Date, end_Date):
	return render_template('accomodation/accomodation_booking_confirm_notif.html', user = user_function.group_User_Info(), accomodation = accom)