'''
Created on Aug 13, 2019

@author: xuwang
'''
import argparse
import csv
import fiona
# from shapely.geometry.polygon import Polygon
from shapely.geometry import shape
#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-sh", "--srcShape", required=True,
    help="source shapefile")
#==============
ap.add_argument("-t", "--targetFolder", required=True,
    help="target folder")
#==============
args = ap.parse_args()
shapeFile = args.srcShape
targetPath = args.targetFolder
finalFile = open(targetPath+"\\plotCenter.csv", 'wt')
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
    writer.writerow(('Plot_ID','X_Plot','Y_Plot'))
    for j in range(0,len(plotIDs)):
        ref_polygon = shape(geoms[j])
        writer.writerow((plotIDs[j],ref_polygon.centroid.coords[0][0],ref_polygon.centroid.coords[0][1]))
finally:
    finalFile.close()
