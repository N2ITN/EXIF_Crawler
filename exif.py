## This module is a work in progress.

## It has the functionality to scan local directories for JPGs, 
## determinine if the JPGs have EXIF data,
## and create a KML file from the GPS points if present
## It is also capable of opening points in Google maps, but only one at a time

# TODO: add functionality for web crawling
# TODO: add multiple point capability to Google maps option
# TODO: unit testing and additional user feedback

import exifread
from geopy import point
import webbrowser
import os






## Option for raw_input:
# kmlName = raw_input("Enter a name for the output KML file, or press enter to skip KML generation: ")
# user = raw_input("Please enter a local path or URL to an EXIF geotagged photo: ").replace("\\","/").replace('"','')
# brows_YN = raw_input("Launch coordinates in browser Y/N: ").lower().replace('yes','y').replace('no','n')


##########
kmlName = 'me'
user = r"C:\Users\zestela53\Downloads".replace("\\","/")
brows_YN = 'n'
##########

lat = ''
lon = ''
lonC = ''
latC = ''
kmlList = []
fileList = []

def testEXIF(image):
	if not image.lower().endswith('.jpg'):
		return False
	try: 
		f = open(image, 'r')
	except IOError:
		print "IOError", image
		return False
	global lat, lon, latC, lonC
	lat = ''
	lon = ''
	lonC = ''
	latC = ''
	tags = exifread.process_file(f)
	for tag in tags:
		if "Lon" in tag:
			if "Ref" not in tag:
				lon = tags[tag]

			else: lonC = str(tags[tag])		

		if "Lat" in tag:
			if "Ref" not in tag:
				lat = tags[tag]

			else: latC = str(tags[tag])
	if lat != '': 
		return True
	return False

def testInput():
	if os.path.isfile(user) == True:

		if testEXIF(user) == True:
			makeCoords(user)

	elif os.path.isdir(user):
		for x,y,z in os.walk(user):
			for item in z:
				if testEXIF(x + "/" + item) == True:
					print True
					makeCoords(item)
				else: pass

def formatCoords(cord):
	out = ''
	cord = str(cord)
	DD = 0
	for part in cord[1:-1].replace(",","").replace("."," ").split(' '):
		if "/" in part:
			part = part.split("/")
			part=  str(int(part[0]) / int(part[1])).replace('.', ' ')
		if DD == 1:
			part = part + "m"
		elif DD == 2:
			part = part + "s"

		out = out + str(part) + " "
		DD+=1

	return out

def makeCoords(file_):
	global lat, lon
	lat= formatCoords(lat)   + latC 
	lon=  formatCoords(lon)  + lonC

	p1  = lat + " " + lon
	p2 = point.Point(p1)
	lat = p2.latitude
	lon = p2.longitude
	lat = float("{0:.8f}".format(lat))
	lon = float("{0:.8f}".format(lon))
	kmlList.append((lon, lat))
	fileList.append(file_)


def output_coords():
	if len(kmlName) > 0:
		import simplekml
		kml = simplekml.Kml()
		for i in range(len(kmlList)):
			thisFile = fileList[i]
			thisPoint = kmlList[i]
			print thisPoint
			try:
				kml.newpoint(name=thisFile, description="--", coords=[thisPoint])
			except TypeError:
				continue
		kml.save(kmlName + ".kml")
		# launchKML = raw_input("Launch KML file, Y/N: ").lower().replace('yes','y').replace('no','n')
		launchKML = 'y'
		if launchKML == 'y':
			os.startfile(kmlName + ".kml")

	if brows_YN == 'y':

		coord_pair = str(lat) + ',' + str(lon)
		url = 'https://www.google.com/maps/place/'+ coord_pair

testInput()
output_coords()
