'''
Created on Nov 16, 2018

@author: xuwang
'''
from qgis.core import *
from qgis.utils import *
from PyQt5.QtCore import *
from qgis.analysis import *
from qgis.gui import *
import numpy as np

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFolder", required=True,
    help="source raster file folder")
args = ap.parse_args()
filePath = args.srcFolder

# try:
#     os.makedirs(str(filePath).replace("orthophotos","orthophotos_RGB"))
#     print("Creating RGB orthophotos directory.")
# except OSError as exception:
#     if exception.errno != errno.EEXIST:
#         raise

QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()

crs = QgsCoordinateReferenceSystem(4326)

exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
print("Total images in the folder: %d" % len(imList))

for im in imList:
    orthoTiffInfo = QFileInfo(im)
    orthoTiffBaseName = orthoTiffInfo.baseName()
    orthoTiffLayer = QgsRasterLayer(im, orthoTiffBaseName)
    
    orthoTiffLayer.renderer().setRedBand(3)
    orthoTiffLayer.renderer().setGreenBand(2)
    orthoTiffLayer.renderer().setBlueBand(1)
    
    renderer = orthoTiffLayer.renderer()
    provider = orthoTiffLayer.dataProvider()
    
    layer_extent = orthoTiffLayer.extent()
    uses_band = renderer.usesBands()
    # print(uses_band)
    
    redType = renderer.dataType(uses_band[0])
    redStats = provider.bandStatistics(uses_band[0], QgsRasterBandStats.All, layer_extent, 0)
    
    greenType = renderer.dataType(uses_band[1])
    greenStats = provider.bandStatistics(uses_band[1], QgsRasterBandStats.All, layer_extent, 0)
    
    blueType = renderer.dataType(uses_band[2])
    blueStats = provider.bandStatistics(uses_band[2], QgsRasterBandStats.All, layer_extent, 0)
    
    pixMin = np.max([redStats.minimumValue, greenStats.minimumValue, blueStats.minimumValue])
    pixMax = np.min([redStats.maximumValue, greenStats.maximumValue, blueStats.maximumValue])
    
    contrast_enhancement = QgsContrastEnhancement.StretchToMinimumMaximum
    
    redEnhancement = QgsContrastEnhancement(redType)
    redEnhancement.setContrastEnhancementAlgorithm(contrast_enhancement,True)
    redEnhancement.setMinimumValue(pixMin)
    redEnhancement.setMaximumValue(pixMax)
    orthoTiffLayer.renderer().setRedContrastEnhancement(redEnhancement)
    
    greenEnhancement = QgsContrastEnhancement(greenType)
    greenEnhancement.setContrastEnhancementAlgorithm(contrast_enhancement,True)
    greenEnhancement.setMinimumValue(pixMin)
    greenEnhancement.setMaximumValue(pixMax)
    orthoTiffLayer.renderer().setGreenContrastEnhancement(greenEnhancement)
    
    blueEnhancement = QgsContrastEnhancement(blueType)
    blueEnhancement.setContrastEnhancementAlgorithm(contrast_enhancement,True)
    blueEnhancement.setMinimumValue(pixMin)
    blueEnhancement.setMaximumValue(pixMax)
    orthoTiffLayer.renderer().setBlueContrastEnhancement(blueEnhancement)
    
    orthoTiffLayer.triggerRepaint()
    
    extent = orthoTiffLayer.extent()
    width = orthoTiffLayer.width()
    height = orthoTiffLayer.height()
    renderer = orthoTiffLayer.renderer()
    provider = orthoTiffLayer.dataProvider()
    crs = orthoTiffLayer.crs()     
    
    pipe = QgsRasterPipe()
    pipe.set(provider.clone())        
    pipe.set(renderer.clone())
    
    renderRasterImage = str(im).replace(".tif","_rgb.tif")
    file_writer = QgsRasterFileWriter(renderRasterImage)
    file_writer.writeRaster(pipe, width, height, provider.extent(), crs)


qgs.exitQgis()

