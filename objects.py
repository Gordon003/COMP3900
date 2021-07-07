from flask import Flask, render_template, request, session, redirect, url_for, Blueprint
from function import data_function, user_function, sort, accom_function, object_function, checker
import os

objects = Blueprint('objects', __name__)

# OBJECT RESULT PAGE
@objects.route('/object/search+<searchType>', methods = ["GET", "POST"])
def object_result(searchType):
	# Get object list
	object_list = object_function.find_Object(searchType)

	# POST Method
	if request.method == "POST":
		editInfo = request.form['submit']

	# GET Method
	return render_template('object/search.html', user = user_function.group_User_Info(), objectList = object_list)

# OBJECT VIEW PAGE
@objects.route('/object/<objectID>', methods = ["GET", "POST"])
def object_view(objectID):
	objects = object_function.get_Object(objectID)
	error = ''
	if request.method == "POST":
		editInfo = request.form['submit']

		# Bidding
		if editInfo == 'bid':
			bid = request.form['price']
			if checker.check_valid_price(bid):
				bid = int(bid)
				if user_function.remove_money(bid) and bid > objects[6] and bid < objects[7] and bid >= objects[4]:
					object_function.bid_Object(objectID, bid)
					objects = object_function.get_Object(objectID)
				else:
					error = 'bid'
			else:
				error = 'bid'
		elif editInfo == 'buyNow':
			buyNow = objects[7]
			if user_function.remove_money(buyNow):
				object_function.buy_Object(objectID, buyNow);
				objects = object_function.get_Object(objectID)
				return redirect(url_for('user.myObject', username = session['username']))
			else:
				error = 'buyNow'


	return render_template('object/object_view.html', user = user_function.group_User_Info(), objects = objects, error = error)