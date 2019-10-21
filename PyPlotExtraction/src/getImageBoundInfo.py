'''
Created on Oct 9, 2018

@author: xuwang
'''
import os
import argparse
from qgis.core import *
from qgis.utils import *
from PyQt5.QtCore import *
from qgis.analysis import *
from qgis.gui import *
import csv

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
# load providers
qgs.initQgis()
crs = QgsCoordinateReferenceSystem(4326)

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFolder", required=True,
    help="source images")
#==============
ap.add_argument("-t", "--targetFile", required=True,
    help="target folder")
#==============
args = ap.parse_args()
filePath = args.srcFolder
finalFile = open(args.targetFile, 'wt')
#------------------------------------------------------------------------
print("File path is: %s" % filePath)
# Create list of all images
exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
print("Total images in the path: %d" % len(imList))
#------------------------------------------------------------------------
try:
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    for im in imList:
        # Ortho raster layer define
        rasterInfo = QFileInfo(im)
        rasterBaseName = rasterInfo.baseName()
        rasterLayer = QgsRasterLayer(im, rasterBaseName)
        if rasterLayer.isValid():
            # print(rasterLayer.extent().toString())
            writer.writerow((im,rasterLayer.extent().toString()))
        else:
            print("Layer failed to load!")
finally:
    finalFile.close()