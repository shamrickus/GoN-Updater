import urllib2, re, sys, json, os, zipFile
from HTMLParser import HTMLParser
from datetime import datetime

urls = ["http://www.moddb.com/mods/glory-of-nephilim/downloads"]
versionFile = "PlugY.ini"
timeFormat = "%d %B %Y"

def updateMod():
	print("Here")

def getCurrentVersion(otherTime):
	if(not os.path.exists("./" + versionFile)):
		sys.exit("Cannot find Plugy File!!")

	with open("./" + versionFile) as f:
		lines = [line.rstrip("\n") for line in f]
		startText = "VersionText=Release: "
		for line in lines:
			if line.startswith(startText):
				line = datetime.strptime(line[len(startText):], timeFormat)
				if(otherTime > line):
					updateMod()
		


class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.match = re.compile('Glory of Nephilim (\d{1}|\d{2}) [A-Za-z]+ 20\d{2}')

	#This the data inbetween attributes
	def handle_data(self, data):
		if(self.match.match(data)):
			data = datetime.strptime(data[len("Glory of Nephilim "):].lower(), timeFormat)
			getCurrentVersion(data)

def wrtieJSON(dump):
	file.write("data.push(" + dump +");\n")

#Strips undefined html attributes and whitespace		
def getFeed(url):
	ret = urllib2.urlopen(url).read().replace("<em>", "").replace("</em>", "").replace("\r", "").replace("<strong>","").replace("</strong>", "").replace("<code>", "").replace("</code>", "").replace("\n","").replace("\t","")
	return ret

if __name__ == "__main__":
	mhp = MyHTMLParser()
	print "Calculating..."

	if(len(sys.argv) == 2 and sys.argv[1] == "debug"):
		debug = True

	for url in urls:
		mhp = MyHTMLParser()
		mhp.feed(getFeed(url))
		
