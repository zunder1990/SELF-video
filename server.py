#!/usr/bin/env python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys
import os
import time
import signal
import subprocess
import re
import shutil



ballroom = "BallroomA"




scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('self-video-zach-208096653289.json', scope)
gc = gspread.authorize(credentials)
gdspreadsheet = gc.open("speakers-list")
worksheet = gdspreadsheet.worksheet(ballroom)

def start():
	filecheck()

def filecheck():
 #This reads the pcaps, pull out the data, and places it into a csv
	#checks for pcap files in incoming

	for fname in os.listdir("/data/video/incoming"):
					if fname.endswith('.mkv'):
						#pcapfile = incomingpath +fname
						talkID = fname.replace(".mkv", "")
						oldfilename ="""/data/video/incoming/"""+fname+""""""
						newfilename ="""/data/video/tmp/"""+fname+"""""" 
						print oldfilename
						print newfilename
						print talkID
						print fname
						shutil.move(oldfilename , newfilename)
						#ffmpegpost(talkID)
						upload(talkID)

#def ffmpegpost(talkID):
#	print "would have done post process with ffmpeg"
	#https://stackoverflow.com/questions/7333232/concatenate-two-mp4-files-using-ffmpeg
	
	#ffmpegcmd1 = """ffmpeg -i ad.mp4 -i """+ talkID +""".raw.mkv -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" """+ talkID +""".withfirstad.mkv"""
	#ffmpegcmd2 = """ffmpeg -i intro.mkv -i """+ talkID +""".withfirstad.mkv -i ad.mkv -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" """+ talkID +""".finished.mkv"""
	#ffmpegcmd1 = """ffmpeg -i /data/video/shared/ad.mkv -i /data/video/tmp/"""+ str(talkID) +""".mkv -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" /data/video/uploadtmp/"""+ str(talkID) +""".uploaded.mkv"""
	#ffmpegcmd1 = """ffmpeg -i /data/video/shared/ad.mkv -i /data/video/tmp/"""+ str(talkID) +""".mkv -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" /data/video/uploadtmp/"""+ str(talkID) +""".uploaded.mkv"""

	
	#print "finished ffmpegpost"
	#subprocess.call(ffmpegcmd1, shell=True)
	#subprocess.call(ffmpegcmd2, shell=True)
	#os.rename("""/data/video/tmp/"""+ str(talkID) +""".mkv""", """/data/video/archive/"""+ str(talkID) +""".raw.mkv""")
	#upload(talkID)
	
def upload(talkID):
	cell = worksheet.find(talkID)

	#print("Found something at R%sC%s" % (cell.row, cell.col))
	
	
	speakername = worksheet.acell("""B""" + str(cell.row) + """ """).value
	talkname = worksheet.acell("""C""" + str(cell.row) + """ """).value
	talkdesc = worksheet.acell("""G""" + str(cell.row) + """ """).value
	print "Speakers name = ", speakername
	print "Talk title = ", talkname
	print "Talk Desc = ", talkdesc
	print "Talk ID = ", talkID
	youtubetitlefull = "" + speakername +" - " + talkname +""
	youtubetitlecapped = youtubetitlefull[:99]
	youtubedesc = """ 2018 SouthEast LinuxFest;  """ + speakername +"""; """ + talkname +"""; """ + talkdesc +""" """
					
	#print "would have ran python upload_video.py --file /home/zach/" + talkID + ".finished.mkv --title " + youtubetitlecapped + " --description " + youtubedesc + " --privacyStatus private"
	print str(talkID)
	uploadcmd = '''python /root/SELF-video/upload_video.py --noauth_local_webserver --file /data/video/tmp/'''+ str(talkID) +'''.mkv --title " ''' + str(youtubetitlecapped) + ''' " --description " ''' + str(youtubedesc) + ''' " --privacyStatus unlisted'''
	print uploadcmd
	subprocess.call(uploadcmd,shell=True)
	os.rename("""/data/video/tmp/"""+ talkID +""".mkv""", """/data/video/archive/"""+ talkID +""".mkv""")
start()