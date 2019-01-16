import praw, requests, re
import urllib
import time
import sys
import os
from PIL import Image
import shutil

amountOfPictures = 100
masterPath = "D:/Reddit/"


file = open('logindata.txt', 'r')
logindata = []
for lines in file:
	logindata.append(lines[:-1])

reddit = praw.Reddit(client_id=logindata[0],
				     client_secret=logindata[1],
					 username=logindata[2],
					 password=logindata[3],
					 user_agent=logindata[4])



subreddit = reddit.subreddit(sys.argv[1])

top = subreddit.top(limit=amountOfPictures)


def makedir():
	try:
		os.mkdir(sys.argv[2])
	except OSError:
		print("Directory allready exists!")
	else: 
		print("Making new directory: ", sys.argv[2])

def checkForFaulty(path):
	#checks if image size is equal to the default imgur "not available" picture
	#if so, it will move image to faulty!
	#also if the image is unopenable, it will too!
	
	try:
		os.mkdir(sys.argv[2] + "/faulty")
	except OSError:
		pass
	try:
		img = Image.open(path)
		width, height = img.size
		if(width*height == 13041):			

			shutil.move(path, sys.argv[2] + "/faulty")
	except: 
		shutil.move(path, sys.argv[2] + "/faulty")

			


for submission in top:
	time.sleep(.1)
	print(submission.url)
	try:
		title = submission.title
		for char in [" ", ".", "!", "?", "/", "*"]
			title.replace(char, "_")

		print(title)
		title = title.encode("utf-8")
		endOfUrl = submission.url[-4:]	

		if(endOfUrl == ".png" or endOfUrl == ".jpg" or endOfUrl == ".gif" ):
			fileFormat = submission.url[-4:]
		elif(submission.url[-5:] == ".JPEG" or submission.url[-5:] == ".gifv"):
			fileFormat = submission.url[-5:]
		else:
			fileFormat = ".png"
			
		pathToFile = '{}{}/{}{}'.format(masterPath, sys.argv[2],title.decode(), fileFormat)
		print(pathToFile)
		urllib.request.urlretrieve(submission.url, pathToFile)
		checkForFaulty(pathToFile)
		
	except Exception as e:
		print("Failed: {}  Reason: {}".format(submission.url, e))