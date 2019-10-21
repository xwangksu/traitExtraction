'''
Created on Jan 8, 2019

@author: xuwang
'''
# import os
from qgis.core import *
from qgis.utils import *
from PyQt5.QtCore import *
from qgis.analysis import *
from qgis.gui import *

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcRaster", required=True,
    help="source raster file")
args = ap.parse_args()
orthoTiff = args.srcRaster

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
# load providers
qgs.initQgis()

crs = QgsCoordinateReferenceSystem(4326)

# Ortho raster layer define
orthoTiffInfo = QFileInfo(orthoTiff)
orthoTiffBaseName = orthoTiffInfo.baseName()
orthoTiffLayer = QgsRasterLayer(orthoTiff, orthoTiffBaseName)
if not orthoTiffLayer.isValid():
    print("Layer failed to load!")
# Tiff saving define
redTiff = str(orthoTiff).replace(".tif","_R.tif")
greenTiff = str(orthoTiff).replace(".tif","_G.tif")
blueTiff = str(orthoTiff).replace(".tif","_B.tif")
# Define each band within the ortho raster layer
entries = []
# Define red band
redBand = QgsRasterCalculatorEntry()
redBand.ref = orthoTiffLayer.name() + '@1'
redBand.raster = orthoTiffLayer
redBand.bandNumber = 1
entries.append(redBand)
# Define green band
greenBand = QgsRasterCalculatorEntry()
greenBand.ref = orthoTiffLayer.name() + '@2'
greenBand.raster = orthoTiffLayer
greenBand.bandNumber = 2
entries.append(greenBand)
# Define blue band
blueBand = QgsRasterCalculatorEntry()
blueBand.ref = orthoTiffLayer.name() + '@3'
blueBand.raster = orthoTiffLayer
blueBand.bandNumber = 3
entries.append(blueBand)
# Generate red Tiff
genRed = QgsRasterCalculator(redBand.ref,
    redTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries)
genRed.processCalculation()
# Generate green Tiff
genGreen = QgsRasterCalculator(greenBand.ref,
    greenTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries)
genGreen.processCalculation()
# Generate blue Tiff
genBlue = QgsRasterCalculator(blueBand.ref,
    blueTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries)
genBlue.processCalculation()


qgs.exitQgis()
