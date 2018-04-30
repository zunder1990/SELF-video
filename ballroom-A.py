#!/usr/bin/env python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys
import os
import time
import signal
import subprocess

encoderurl = 'rtsp://10.60.0.49:554/main'
camurl = 'rtsp://10.60.0.52:7447/5ac91bd5ec2e84e0ab7649cb_0'

ballroom = "BallroomA"

starttimes = ["8:00", "9:15", "13:00", "14:00", "04-27-10:26"]


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('self-video-zach-208096653289.json', scope)
gc = gspread.authorize(credentials)
gdspreadsheet = gc.open("speakers-list")
worksheet = gdspreadsheet.worksheet(ballroom)

def start():
	#worksheet_list = gdspreadsheet.worksheets()
	#print worksheet_list
	
	
	#currentdate = datetime.now().strftime('%m-%d')
	#print timestamp
	checklist()



#This will check the list to see if the current time matches a time in the list
def checklist():
	while True:
		currenttime = datetime.now().strftime('%m-%d-%H:%M')
		print "time now = ", currenttime
		if currenttime in starttimes:
			print "current time in list = ", currenttime
			googlesheetlookup() 
			break

def googlesheetlookup():
	currenttime = datetime.now().strftime('%m-%d-%H:%M')
	cell = worksheet.find(currenttime)

	#print("Found something at R%sC%s" % (cell.row, cell.col))
	
	
	#speakername = worksheet.acell("""B""" + str(cell.row) + """ """).value
	#talkname = worksheet.acell("""C""" + str(cell.row) + """ """).value
	#talkdesc = worksheet.acell("""G""" + str(cell.row) + """ """).value
	#talkdate = worksheet.acell("""E""" + str(cell.row) + """ """).value
	#talktime = worksheet.acell("""F""" + str(cell.row) + """ """).value
	talkID = worksheet.acell("""A""" + str(cell.row) + """ """).value
	#print "Speakers name = ", speakername
	#print "Talk title = ", talkname
	#print "Talk Desc = ", talkdesc
	#print "Talk date = ", talkdate
	#print "Talk time = ", talktime
	print "Talk ID = ", talkID
	#return talkID
	ffmpegrecord(talkID)

def ffmpegrecord(talkID):
	#print "would have started ffmpeg with file "+ talkID +".mkv"
	#print """this is what would have been ran  ffmpeg  -rtsp_transport tcp -i '"""+ camurl +"""' -i '""" + encoderurl + """' -filter_complex "[0]scale=iw/4:ih/4 [pip]; [1][pip]overlay=main_w-overlay_w-10:main_h-overlay_h-10" -y """+ talkID +""".mkv"""
	#time.sleep(20)#seconds to mock the time for ffmpeg to record
	cmd1 = """ffmpeg  -rtsp_transport tcp -i '"""+ camurl +"""' -i '""" + encoderurl + """' -filter_complex "[0]scale=iw/4:ih/4 [pip]; [1][pip]overlay=main_w-overlay_w-10:main_h-overlay_h-10" -y """+ talkID +""".raw.mkv"""
	ffmpegrecordcmd = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
	time.sleep(3600)#seconds= 1 hour
	os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
	ffmpegpost(talkID)

def ffmpegpost(talkID):
	print "would have done post process with ffmpeg"
	#https://stackoverflow.com/questions/7333232/concatenate-two-mp4-files-using-ffmpeg
	
	ffmpegcmd1 = """ffmpeg -i ad.mp4 -i """+ talkID +""".raw.mkv -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" """+ talkID +""".withfirstad.mkv"""
	ffmpegcmd2 = """ffmpeg -i intro.mkv -i """+ talkID +""".withfirstad.mkv -i ad.mkv -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" """+ talkID +""".finished.mkv"""
	subprocess.call(ffmpegcmd1, shell=True)
	subprocess.call(ffmpegcmd2, shell=True)
	upload(talkID)
	
def upload(talkID):
	cell = worksheet.find(talkID)

	#print("Found something at R%sC%s" % (cell.row, cell.col))
	
	
	speakername = worksheet.acell("""B""" + str(cell.row) + """ """).value
	talkname = worksheet.acell("""C""" + str(cell.row) + """ """).value
	talkdesc = worksheet.acell("""F""" + str(cell.row) + """ """).value
	print "Speakers name = ", speakername
	print "Talk title = ", talkname
	print "Talk Desc = ", talkdesc
	print "Talk ID = ", talkID
	youtubetitlefull = "" + speakername +" - " + talkname +""
	youtubetitlecapped = youtubetitlefull[:99]
	youtubedesc = " 2018 SouthEast LinuxFest;  " + speakername +"; " + talkname +"; " + talkdesc +" "
					
	#print "would have ran python upload_video.py --file /home/zach/" + talkID + ".finished.mkv --title " + youtubetitlecapped + " --description " + youtubedesc + " --privacyStatus private"
	uploadcmd = """upload_video.py --file /home/zach/""" + talkID + """.finished.mkv --title """ + youtubetitlecapped + """ --description """ + youtubedesc + """ --privacyStatus unlisted"""
	subprocess.call(uploadcmd)

start()