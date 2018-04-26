#!/usr/bin/env python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys
import os
import time

encoderurl = 'rtsp://10.60.0.49:554/main'
camurl = 'rtsp://10.60.0.52:7447/5ac91bd5ec2e84e0ab7649cb_0'

ballroom = "BallroomA"

starttimes = ["8:00", "9:15", "13:00", "14:00", "13:37"]


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('self-video-zach-208096653289.json', scope)
gc = gspread.authorize(credentials)
gdspreadsheet = gc.open("speakers-list")
worksheet = gdspreadsheet.worksheet(ballroom)

#This will check the list to see if the current time matches a time in the list
def checklist():
	currenttime = datetime.now().strftime('%H:%M')
	if currenttime in starttimes:
			print "current time in list = ", currenttime
			googlesheetlookup()
	time.sleep(20)#seconds
	checklist()

def googlesheetlookup():
	currenttime = datetime.now().strftime('%H:%M')
	cell = worksheet.find(currenttime)

	#print("Found something at R%sC%s" % (cell.row, cell.col))
	
	
	speakername = worksheet.acell("""B""" + str(cell.row) + """ """).value
	talkname = worksheet.acell("""C""" + str(cell.row) + """ """).value
	talkdesc = worksheet.acell("""G""" + str(cell.row) + """ """).value
	talkdate = worksheet.acell("""E""" + str(cell.row) + """ """).value
	talktime = worksheet.acell("""F""" + str(cell.row) + """ """).value
	print "Speakers name = ", speakername
	print "Talk title = ", talkname
	print "Talk Desc = ", talkdesc
	print "Talk date = ", talkdate
	print "Talk time = ", talktime
	
def start():
	#worksheet_list = gdspreadsheet.worksheets()
	#print worksheet_list
	
	
	#currentdata = datetime.now().strftime('%m-%d')
	#print timestamp
	checklist()
	
start()