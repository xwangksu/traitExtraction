'''
Created on Jan 11, 2019

@author: xuwang
'''
import os
import argparse
import exiftool
import csv
#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFolder", required=True,
    help="source raster files folder")
ap.add_argument("-tf", "--targetFolder", required=True,
    help="target folder")
args = ap.parse_args()
filePath = args.srcFolder
targetPath = args.targetFolder
#------------------------------------------------------------------------
# Create list of total images
exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(name) # os.path.join(dirpath, name))
print("Total images in the path: %d" % len(imList))
finalFile = open(os.path.join(targetPath, "orthophotoCoord.csv"),'wt')
try:
        # print(et.get_metadata(imFile))
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    # Header row if needed
    writer.writerow(('Original_file','Longitude','Latitude','Altitude'))
    with exiftool.ExifTool() as et:
        for im in imList:
            imFile = os.path.join(dirpath, im)
            # print(im)
            # print(et.get_metadata(imFile))
            # dtTags = et.get_tag('EXIF:DateTimeOriginal',imFile)
            gpsLongi = float(et.get_tag('EXIF:GPSLongitude', imFile))
            gpsLongiRef = str(et.get_tag('EXIF:GPSLongitudeRef', imFile))
            gpsLati = float(et.get_tag('EXIF:GPSLatitude', imFile))
            gpsLatiRef = str(et.get_tag('EXIF:GPSLatitudeRef', imFile))
            gpsAlti = float(et.get_tag('EXIF:GPSAltitude', imFile))
            gpsAltiRef = float(et.get_tag('EXIF:GPSAltitudeRef', imFile))
            if gpsLongiRef =="W":
                gpsLongi = gpsLongi * (-1)
            if gpsLatiRef =="S":
                gpsLati = gpsLati * (-1)
            gpsAlti = gpsAlti - gpsAltiRef
            # Save output file
            writer.writerow((im, gpsLongi, gpsLati, gpsAlti))
finally:
    finalFile.close()
