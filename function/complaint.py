from flask import session
import sqlite3

def send_Complaint(complaintID, text, complaintType):

	conn = sqlite3.connect('data/main_data.db')
	insertStatement = 'INSERT INTO complaint(type,complainerID,complaintID,description,solved) VALUES(?,?,?,?,?)'
	data = [(complaintType,session['accID'],complaintID,text,0)]
	conn.executemany(insertStatement, data)
	conn.commit()

	return