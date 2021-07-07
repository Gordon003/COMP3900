from flask import Flask, render_template, request, session, redirect, url_for, Blueprint
from function import data_function, user_function, sort, accom_function, object_function, checker, complaint
from werkzeug.utils import secure_filename
import os
from os.path import join

user = Blueprint('user', __name__)

# LOGOUT PAGE
@user.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

# LOGIN PAGE
@user.route('/login', methods = ["GET", "POST"])
def login():
	# POST Method
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']

		# Check validity
		if username == '' or password == '' or not checker.check_Correct_User(username, password):
			return render_template('home/login.html', error = "No username or password entered")
		else:
			return redirect(url_for("index"))

	# GET Method
	return render_template('home/login.html')

# NEW USER PAGE
@user.route('/join', methods = ["GET", "POST"])
def join():
	# POST Method
	if request.method == "POST":
		# Get user input
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']
		phone = request.form['phone']
		address = request.form['address']
		email = request.form['email']
		fname = ''
		if 'file' in request.files:
			file = request.files['file']
			fname = file.filename

		combine_list = [username, phone, address, email]
		error = ''
		
		# Check unique name
		if not checker.check_unique_name(username):
			error = "Username either already existed or not inputed"
		# Check password matched
		if not checker.check_valid_password(password) or password != password2:
			error = "Password are either not matched to each other or not inputed"
		# Phone
		if not checker.check_valid_phone(phone):
			error = 'Phone number not inputed or not at right format.'
		# Address
		if not checker.check_valid_address(address):
			error = "Address not inputed or doesn't existed."
		# Email
		if not checker.check_valid_email(email):
			error = 'Email not inputed or not at right format.'
		# Icon
		if fname == '':
			error = 'Icon not inputed'

		# If there are error
		if error != '':
			return render_template('home/new_user.html', error = error, previousInput = combine_list)			

		# Save image
		filename = secure_filename(file.filename)
		fname = username + '.png'
		path = 'static/images/user/'
		file.save(os.path.join(path, fname))

		# Add user to database
		user_function.add_User(username, password, phone, address, email)
		return redirect(url_for('index'))

	# GET Method
	return render_template('home/new_user.html') 

# PROFILE PAGE
@user.route('/<username>')
def profile(username):
	otherUser = user_function.get_User(username)
	print(otherUser)
	if session and username == session['username']:
		return render_template('user/profile.html', user = user_function.group_User_Info(), username = username)
	# No such user
	elif not otherUser:
		return render_template('user/profile.html', user = user_function.group_User_Info(), username = username, error = 1)
	# Access other user profile
	else:
		return render_template('user/profile.html', user = user_function.group_User_Info(), otherUser = otherUser, username = username)


# EDIT USER INFO
@user.route('/<username>/edit', methods = ["GET", "POST"])
def editUser(username):
	error = ''

	# POST Method
	if request.method =="POST":
		editInfo = request.form['submit']

		# Update username
		if editInfo == 'name':
			username = request.form['username']
			if (username==session['username']) or (username==''):
				error = 'name'
			else:
				oldUsername = session['username']
				if user_function.update_Username(username):
					fname = oldUsername + '.png'
					newfname = username + '.png'
					path = 'static/images/user/'
					filenames = os.listdir(path)

					for filename in filenames:
						if (filename == fname):
							os.rename(os.path.join(path,filename), os.path.join(path,newfname))

				return redirect(url_for('user.editUser', username = session['username']))

		# Update password
		elif editInfo == 'password':
			pass1 = request.form['password1']
			pass2 = request.form['password2']
			if (pass1=='') or (pass2=='') or (pass1!=pass2) or (pass1==session['password'] or not checker.check_valid_password(pass1)):
				error = 'password'
			else:
				user_function.update_Password(request.form['password1'], request.form['password2'])
				return redirect(url_for('user.editUser', username = session['username']))

		# Update phone #
		elif editInfo == 'phone':
			phone = request.form['phone']
			if phone == '' or not checker.check_valid_phone(phone):
				error = 'phone'
			else:
				user_function.update_Phone(phone)
				return redirect(url_for('user.editUser', username = session['username']))

		# Update Address
		elif editInfo == 'address':
			address = request.form['address']
			address = address.lower()
			if address=='' or not checker.check_valid_address(address):
				error = 'address'
			else:
				user_function.update_Address(address)
				return redirect(url_for('user.editUser', username = session['username']))

		# Update email
		elif editInfo == 'email':
			email = request.form['email']
			if email==''  or not checker.check_valid_email(email):
				error = 'email'
			else:
				user_function.update_Email(email)
				return redirect(url_for('user.editUser', username = session['username']))

	# GET Method
	return render_template('user/edit_user.html', user = user_function.group_User_Info(), username = username, error = error)

# ADD TO USER BALANCE
@user.route('/<username>/recharge', methods = ["GET", "POST"])
def rechargeMoney(username):
	error = ''

	# POST Method
	if request.method =="POST":
		money = request.form['money']
		print(money.isdigit() )
		if money.isdigit():
			if int(money) > 0 and int(money) <= 800:
				user_function.add_money(int(money))
			else:
				error = 'money'
		else:
			error = 'money'

	return render_template('user/recharge_money.html', user = user_function.group_User_Info(), username = username, error = error)

# VIEW USER ACCMODATION
@user.route('/<username>/myAccomodation')
def myAccomodation(username):
	myAccomodationList = accom_function.find_MyAccomodation(username)
	return render_template('user/myAccom.html', user = user_function.group_User_Info(), username = username, accomodationList = myAccomodationList)

# VIEW USER ACCOMODATION BOOKING
@user.route('/<username>/check_Accom/<accID>')
def myAccomodationBooking(username, accID):
	accomodation = accom_function.get_Accomodation(accID)
	confirmedBooking = accom_function.find_otherPeopleConfirmedBooking2(accID)
	return render_template('accomodation/accomodation_booking_check.html', user = user_function.group_User_Info(), username = username, accomodation = accomodation , confirmedBooking = confirmedBooking)


# VIEW USER OBJECT
@user.route('/<username>/myObject')
def myObject(username):
	myObjectList = object_function.find_MyObject(username)
	return render_template('user/myObject.html', user = user_function.group_User_Info(), username = username, objectList = myObjectList)

# VIEW USER ACCOMODATION NOTIFICATION
@user.route('/<username>/my_Accomodation_Notification')
def myAccomNotification(username):
	waitBooking = accom_function.find_myWaitBooking(session['accID'])
	otherPeopleBooking = accom_function.find_otherPeopleBooking(session['accID'])
	rejectedBooking = accom_function.find_myRejectedBooking()
	return render_template('user/user_accom_notification.html', user = user_function.group_User_Info(), username = username, waitBooking = waitBooking, otherPeopleBooking=otherPeopleBooking, rejectedBooking = rejectedBooking)

# VIEW USER ACCOMODATION NOTIFICATION
@user.route('/<username>/my_Booking')
def myConfirmedBooking(username):
	yourBooking = accom_function.find_myConfirmedBooking(session['accID'])
	return render_template('user/user_booking.html', user = user_function.group_User_Info(), username = username, yourBooking = yourBooking)

# VIEW USER OBJECT NOTIFICATION
@user.route('/<username>/my_Object_Notification')
def myObjectNotification(username):
	object_list = object_function.get_Bid_Object(1)
	mySoldObject = object_function.find_MySoldObject(username)
	print(object_list)
	return render_template('user/user_object_notification.html', user = user_function.group_User_Info(), username = username, object_list = object_list, mySoldObject = mySoldObject)

# VIEW USER ACCOMODATION NOTIFICATION
@user.route('/<username>/my_Bought_Object')
def myBoughtObject(username):
	yourBooking = accom_function.find_myConfirmedBooking(username)
	return render_template('user/user_object_bought.html', user = user_function.group_User_Info(), username = username, yourBooking = yourBooking)

# REPORT USER
@user.route('/<username>/report', methods = ["GET", "POST"])
def user_report(username):

	user = user_function.get_User(username)

	if request.method == 'POST':
		complaint_info = request.form['complaint']
		if complaint_info != "":
			complaint.send_Complaint(user_function.get_UserID_name(username), complaint_info, "user")
			return render_template('user/user_report_confirm_notif.html', user = user_function.group_User_Info())


	return render_template('user/user_report.html', user = user_function.group_User_Info(), reportedUser = user)

# USER ACCEPT BOOKING
@user.route('/<username>/<bookingID>/accept')
def acceptBooking(username, bookingID):
	accom_function.accept_Booking(bookingID)
	return redirect(url_for('user.myAccomNotification', username = session['username']))


# USER REJECT BOOKING
@user.route('/<username>/<bookingID>/reject')
def rejectBooking(username, bookingID):
	accom_function.reject_Booking(bookingID)
	return redirect(url_for('user.myAccomNotification', username = session['username']))

# CANCEL
@user.route('/<username>/<bookingID>/cancel')
def cancel_Booking(username, bookingID):
	accom_function.reject_Booking(bookingID)
	return redirect(url_for('user.myConfirmedBooking', username = session['username']))

# REMOVE
@user.route('/<username>/<bookingID>/remove')
def remove_Booking(username, bookingID):
	accom_function.remove_Booking(bookingID)
	return redirect(url_for('user.myAccomNotification', username = session['username']))

# USER ADD NEW ACCOMODATION
@user.route('/<username>/add_New_Accom', methods = ["GET", "POST"])
def addAccomodation(username):
	# POST Method
	if request.method == "POST":
		address = request.form['address']
		bedroom = request.form['bedroom']
		washroom = request.form['washroom']
		price = request.form['price']
		houseType = request.form['type']
		description = request.form['description']
		combine_list = [address, bedroom, washroom, price, houseType, description]
		
		# Validity
		error = ""
		if address == "" or not checker.check_valid_address(address.lower()):
			error = "address"
		elif str(price) == "" or not checker.check_valid_price(price):
			error = "price"
		elif description == "":
			error = "description"
		elif 'mainImage' not in request.files or 'sideImage1' not in request.files or 'sideImage2' not in request.files or 'sideImage3' not in request.files:
			error = "image"
		elif not user_function.remove_money(10):
			error = "money"
		
		if error != "":
			return render_template('accomodation/new_accomodation.html', user = user_function.group_User_Info(), username = username, previousInput = combine_list, error = error)

		# Save image
		mainImage = request.files['mainImage']
		mainImageName = mainImage.filename
		sideImage1 = request.files['sideImage1']
		sideImage1Name = sideImage1.filename
		sideImage2 = request.files['sideImage2']
		sideImage2Name = sideImage2.filename
		sideImage3 = request.files['sideImage3']
		sideImage3Name = sideImage3.filename

		# Add accomodation into database
		accID = accom_function.add_Accomodation(username, address.lower(), bedroom, washroom, description, price, houseType)

		# Add Image
		path = 'static/images/accomodation/' + str(accID) 
		os.mkdir(path)
		mainFile = secure_filename(mainImage.filename)
		mainImage.save(os.path.join(path,'main.png'))
		side1File = secure_filename(sideImage1.filename)
		sideImage1.save(os.path.join(path,'side1.png'))
		side2File = secure_filename(sideImage2.filename)
		sideImage2.save(os.path.join(path,'side2.png'))
		side3File = secure_filename(sideImage3.filename)
		sideImage3.save(os.path.join(path,'side3.png'))

		return redirect(url_for('user.myAccomodation', username = username))

	return render_template('accomodation/new_accomodation.html', user = user_function.group_User_Info(), username = username, error = "")

# EDIT ACCOMODATION
@user.route('/<username>/edit_Accom/<accID>', methods = ["GET", "POST"])
def edit_Accomodation(username, accID):
	error = ''
	# POST Method
	if request.method =="POST":
		editInfo = request.form['submit']
		error = ''
		# Update address
		if editInfo == 'address':
			address = request.form['address']
			if address == '' or not checker.check_valid_address(address):
				error = 'address'
			else:
				accom_function.update_Acc_Address(accID, address)

		# Update password
		elif editInfo == 'bedroom':
			bedroom = request.form['bedroom']
			accom_function.update_Acc_Bedroom(accID, bedroom)

		# Update washroom
		elif editInfo == 'washroom':
			washroom = request.form['washroom']
			accom_function.update_Acc_Washroom(accID, washroom)

		# Update price
		elif editInfo == 'price':
			price = request.form['price']
			if checker.check_valid_price(price):
				accom_function.update_Acc_Price(accID, price)
			else:
				error = 'price'

		# Update description
		elif editInfo == 'description':
			description = request.form['description']
			if description == "":
				error = 'description'
			else:
				accom_function.update_Acc_Description(accID, description)

		if error != "":
			accomodation = accom_function.get_Accomodation(accID)
			return render_template('accomodation/edit_accom.html', user = user_function.group_User_Info(), accomodation = accomodation, error = error)

	# GET Method
	accomodation = accom_function.get_Accomodation(accID)
	return render_template('accomodation/edit_accom.html', user = user_function.group_User_Info(), accomodation = accomodation)

# USER REMOVE ACCOMODATION
@user.route('/<username>/delete_Accom/<accID>')
def deleteAccomodation(username,accID):
	accom_function.remove_Accomodation(accID)
	user_function.add_money(10)
	return redirect(url_for('user.myAccomodation', username = username))

# USER ADD NEW OBJECT
@user.route('/<username>/add_New_Object', methods = ["GET", "POST"])
def addObject(username):

	if request.method == "POST":
		address = request.form['address']
		minimumPrice = request.form['minimumPrice']
		buyNowPrice = request.form['buyNowPrice']
		objectType = request.form['type']
		description = request.form['description']

		combine_list = [address, minimumPrice, buyNowPrice, objectType, description]

		# Validity
		error = ""
		if address == "" or not checker.check_valid_address(address):
			error = "address"
		elif str(minimumPrice) == "" or not checker.check_valid_price(minimumPrice):
			error = "minimumPrice"
		elif str(buyNowPrice) == "" or not checker.check_valid_price(buyNowPrice) or buyNowPrice < minimumPrice:
			error = "buyNowPrice"
		elif description == "":
			error = "description"
		elif 'mainImage' not in request.files or 'sideImage1' not in request.files:
			error = "image"
		elif not user_function.remove_money(5):
			error = "money"

		if error != "":
			object_list = data_function.get_Object()
			return render_template('object/new_object.html', user = user_function.group_User_Info(), username = username, previousInput = combine_list, error = error, object_list = object_list)

		# Save image	
		mainImage = request.files['mainImage']
		mainImageName = mainImage.filename
		sideImage1 = request.files['sideImage1']
		sideImage1Name = sideImage1.filename

		# Add accomodation into database
		objectID = object_function.add_Object(username, address.lower(), description, minimumPrice, buyNowPrice, objectType.lower())

		# Add static image
		path = 'static/images/object/' + str(objectID) 
		os.mkdir(path)
		mainFile = secure_filename(mainImage.filename)
		mainImage.save(os.path.join(path,'main.png'))
		side1File = secure_filename(sideImage1.filename)
		sideImage1.save(os.path.join(path,'side1.png'))

		return redirect(url_for('user.myObject', username = username))

	object_list = data_function.get_Object()
	return render_template('object/new_object.html', user = user_function.group_User_Info(), username = username, object_list = object_list)

# EDIT OBJECT
@user.route('/<username>/edit_Object/<objectID>', methods = ["GET", "POST"])
def edit_Object(username, objectID):
	error = ''
	# POST Method
	if request.method =="POST":
		editInfo = request.form['submit']

		# Update address
		if editInfo == 'address':
			address = request.form['address']
			if address =='' or not checker.check_valid_address(address):
				error = 'address'
			else:
				object_function.update_Object_Address(objectID, address)
				return redirect(url_for('user.edit_Object', username = session['username'], objectID = objectID))

		# Update description
		elif editInfo == 'description':
			description = request.form['description']
			if description == '':
				error = 'description'
			else:
				object_function.update_Object_Description(objectID, description)
				return redirect(url_for('user.edit_Object', username = session['username'], objectID = objectID))

	# GET Method
	myObject = object_function.get_Object(objectID)[0]
	return render_template('object/edit_Object.html', user = user_function.group_User_Info(), myObject = myObject, error = error)

# USER REMOVE ACCOMODATION
@user.route('/<username>/delete_Object/<objectID>')
def deleteObject(username,objectID):
	object_function.remove_Object(objectID)
	user_function.add_money(5)
	return redirect(url_for('user.myObject', username = username))