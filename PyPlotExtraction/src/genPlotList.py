'''
Created on Oct 8, 2018

@author: xuwang
'''
import argparse
import numpy
import csv
import fiona
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape
#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFile", required=True,
    help="source file of image bound info")
#==============
ap.add_argument("-sh", "--shape", required=True,
    help="field map shapefile")
#==============
ap.add_argument("-t", "--targetFolder", required=True,
    help="target folder")
#==============
args = ap.parse_args()
plotBoundFile = args.srcFile
shapeFile = args.shape
targetPath = args.targetFolder
finalFile = open(targetPath+"\\imagePlotList.csv", 'wt')
#------------------------------------------------------------------------
with fiona.open(shapeFile) as shapes:
    geoms = [feature["geometry"] for feature in shapes]
    plotIDs = [feature["properties"] for feature in shapes]
# plotShapes = []
for i in range(len(plotIDs)):
    plotIDs[i] = str(plotIDs[i]).split("'")[3] ##### -->?
#------------------------------------------------------------------------
try:
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    imNum = 0
    imageBoundInfo = open(plotBoundFile,'r')
    for ibLine in imageBoundInfo:
        imNum += 1
        ib = ibLine.split(',"')
        # Image file name
        imageFile = str(ib[0]).replace("\\", "/")
        imageFileElement = imageFile.split("/")
        imageID = imageFileElement[len(imageFileElement)-1]
        # Image coordinates
        imageBound = str(ib[1]).split(' : ')
        imLong_1 = float(imageBound[0].split(',')[0])
        imLat_1 = float(imageBound[0].split(',')[1])
        imLong_2 = float(imageBound[1].split(',')[0])
        imLat_2 = imageBound[1].split(',')[1]
        imLat_2 = float(imLat_2.rstrip('"\n'))
        # create polygon
        x_min = numpy.min([imLong_1,imLong_2])
        x_max = numpy.max([imLong_1,imLong_2])
        y_min = numpy.min([imLat_1,imLat_2])
        y_max = numpy.max([imLat_1,imLat_2])
        # Buffer
        xb_min = x_min+0.1*(x_max-x_min)
        xb_max = x_max-0.1*(x_max-x_min)
        yb_min = y_min+0.1*(y_max-y_min)
        yb_max = y_max-0.1*(y_max-y_min)
        imPolygon = Polygon([(xb_min, yb_min), (xb_max, yb_min), (xb_max, yb_max), (xb_min, yb_max)])
        # print(imPolygon)
        plotList = ""
        for j in range(0,len(plotIDs)):
            if imPolygon.contains(shape(geoms[j])):
                plotList = plotList+plotIDs[j]+","
        if plotList != "":
            print(str(imNum)+" "+imageID+ " "+plotList)
            writer.writerow((imageFile,plotList))  
finally:
    finalFile.close()
