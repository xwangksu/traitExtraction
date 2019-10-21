'''
Created on Oct 8, 2018

@author: xuwang
'''
import argparse
import fiona
import rasterio
from rasterio.mask import mask
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFile", required=True,
    help="source image-plot list")
#==============
ap.add_argument("-shp", "--shapeFile", required=True,
    help="source shapefile")
#==============
ap.add_argument("-tpath", "--targetPath", required=True,
    help="target path")
#==============
args = ap.parse_args()
srcFile = args.srcFile
plotShape = args.shapeFile
targetFolder = args.targetPath
#------------------------------------------------------------------------
with fiona.open(plotShape) as shapes:
    geoms = [feature["geometry"] for feature in shapes]
    plotIDs = [feature["properties"] for feature in shapes]
for i in range(len(plotIDs)):
    plotIDs[i] = str(plotIDs[i]).split("'")[3]
#------------------------------------------------------------------------
imagePlotList = open(srcFile,'r')
nline = 0
for eline in imagePlotList:
    nline += 1
    elineElement = eline.split(',"')
    imageFile = str(elineElement[0])
    imageFileElement = imageFile.split("/")
    imageID = imageFileElement[len(imageFileElement)-1]
    targetPlotIDs = str(elineElement[1]).split(',') # .replace("\n","")
    print(nline)
    for tp in targetPlotIDs:
        try:
            with rasterio.open(imageFile) as srcRaster:
                out_image, out_transform = mask(srcRaster, [geoms[plotIDs.index(tp)]], crop = True)
            out_meta = srcRaster.meta.copy()
            if out_image.shape[1]>0 and out_image.shape[2]>0:
                out_meta.update({"driver": "GTiff", "height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})
                if tp.find("/") != -1:
                    pid = tp.replace("/","$$$")
                else:
                    pid = tp
                with rasterio.open(targetFolder+"\\"+pid+"-"+imageID, "w", **out_meta) as dest:
                    dest.write(out_image)
        except:
            pass
