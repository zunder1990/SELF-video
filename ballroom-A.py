#!/usr/bin/env python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

encoderurl = 'rtsp://10.60.0.49:554/main'
camurl = 'rtsp://10.60.0.52:7447/5ac91bd5ec2e84e0ab7649cb_0'

ballroom = "BallroomA"


credentials = ServiceAccountCredentials.from_json_keyfile_name('self-video-zach-208096653289.json', scope)
gc = gspread.authorize(credentials)
gdspreadsheet = gc.open("speakers-list")

def start():
	#worksheet_list = gdspreadsheet.worksheets()
	#print worksheet_list
	worksheet = gdspreadsheet.worksheet(ballroom)
	cell = worksheet.find("13:00")

	print("Found something at R%sC%s" % (cell.row, cell.col))
	
	
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


	
start()