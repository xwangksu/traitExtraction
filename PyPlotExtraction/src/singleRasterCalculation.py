'''
Created on Oct 9, 2018

@author: xuwang
'''
# import os
from qgis.core import *
from qgis.utils import *
from PyQt5.QtCore import *
from qgis.analysis import *
from qgis.gui import *

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
# load providers
qgs.initQgis()

crs = QgsCoordinateReferenceSystem(4326)
imgSrcPath = 'G:/2018_KS_Wheat/20180423_18ASH_BYD/test/'
orthoTiff = imgSrcPath+'CAM_RM01-1743026-SC_20180423_161932_IMG_0200_1.tif'
# Ortho raster layer define
orthoTiffInfo = QFileInfo(orthoTiff)
orthoTiffBaseName = orthoTiffInfo.baseName()
orthoTiffLayer = QgsRasterLayer(orthoTiff, orthoTiffBaseName)
if not orthoTiffLayer.isValid():
    print("Layer failed to load!")
#dateStamp = ['20180813']
#loc='_Ash_NAM_'
#for ds in dateStamp:
# Tiff saving define
redTiff = imgSrcPath+'R.tif'
greenTiff = imgSrcPath+'G.tif'
blueTiff = imgSrcPath+'B.tif'
redEdgeTiff = imgSrcPath+'RE.tif'
nirTiff = imgSrcPath+'Nir.tif'
ndviTiff = imgSrcPath+'NDVI.tif'
ndreTiff = imgSrcPath+'NDRE.tif'
gNDVITiff = imgSrcPath+'GNDVI.tif'
# Define each band within the ortho raster layer
entries = []
# Define red band
redBand = QgsRasterCalculatorEntry()
redBand.ref = orthoTiffLayer.name()+'@3'
redBand.raster = orthoTiffLayer
redBand.bandNumber = 3
entries.append(redBand)
# Define green band
greenBand = QgsRasterCalculatorEntry()
greenBand.ref = orthoTiffLayer.name()+'@2'
greenBand.raster = orthoTiffLayer
greenBand.bandNumber = 2
entries.append(greenBand)
# Define blue band
blueBand = QgsRasterCalculatorEntry()
blueBand.ref = orthoTiffLayer.name()+'@1'
blueBand.raster = orthoTiffLayer
blueBand.bandNumber = 1
entries.append(blueBand)
# Define redEdge band
redEdgeBand = QgsRasterCalculatorEntry()
redEdgeBand.ref = orthoTiffLayer.name()+'@4'
redEdgeBand.raster = orthoTiffLayer
redEdgeBand.bandNumber = 5
entries.append(redEdgeBand)
# Define Nir band
nirBand = QgsRasterCalculatorEntry()
nirBand.ref = orthoTiffLayer.name()+'@5'
nirBand.raster = orthoTiffLayer
nirBand.bandNumber = 4
entries.append(nirBand)
# Generate red Tiff
genRed = QgsRasterCalculator( redBand.ref,
    redTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genRed.processCalculation()
# Generate green Tiff
genGreen = QgsRasterCalculator( greenBand.ref,
    greenTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genGreen.processCalculation()
# Generate blue Tiff
genBlue = QgsRasterCalculator( blueBand.ref,
    blueTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genBlue.processCalculation()
# Generate redEdge Tiff
genRedEdge = QgsRasterCalculator( redEdgeBand.ref,
    redEdgeTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genRedEdge.processCalculation()
# Generate Nir Tiff
genNir = QgsRasterCalculator( nirBand.ref,
    nirTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genNir.processCalculation()
# Generate NDVI Tiff
genNDVI = QgsRasterCalculator( '( '+nirBand.ref+' - '+redBand.ref+' ) / ( '+nirBand.ref+' + '+redBand.ref+' )',
    ndviTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genNDVI.processCalculation()
# Generate GNDVI Tiff
genGNDVI = QgsRasterCalculator( '( '+nirBand.ref+' - '+greenBand.ref+' ) / ( '+nirBand.ref+' + '+greenBand.ref+' )',
    gNDVITiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genGNDVI.processCalculation()
# Generate NDRE Tiff
genNDRE = QgsRasterCalculator( '( '+nirBand.ref+' - '+redEdgeBand.ref+' ) / ( '+nirBand.ref+' + '+redEdgeBand.ref+' )',
    ndreTiff, 'GTiff', orthoTiffLayer.extent(), orthoTiffLayer.width(), orthoTiffLayer.height(), entries )
genNDRE.processCalculation()

qgs.exitQgis()