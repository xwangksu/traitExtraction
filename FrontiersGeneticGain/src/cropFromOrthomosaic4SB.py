'''
Created on Jan 8, 2019

@author: xuwang
'''
import argparse
import fiona
import rasterio
from rasterio.mask import mask
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-sgt", "--geoTiff", required=True,
    help="Source GeoTiff image")
#==============
ap.add_argument("-shp", "--shapeFile", required=True,
    help="source shapefile")
#==============
ap.add_argument("-tpath", "--targetPath", required=True,
    help="target path")
#==============
args = ap.parse_args()
srcGeoTiff = args.geoTiff
plotShape = args.shapeFile
targetFolder = args.targetPath
# 
with fiona.open(plotShape) as shapes:
    geoms = [feature["geometry"] for feature in shapes]
    plotIDs = [feature["properties"] for feature in shapes]
# print(geoms[0])
# print(len(geoms))
for i in range(len(plotIDs)):
    plotID = str(plotIDs[i]).split(" ")[1].split(")")[0]
    print(plotID)
    if plotID.find("/") != -1:
        plotID = plotID.replace("/","-")
        print(plotID)
    # load the raster, mask it by the polygon and crop it
    with rasterio.open(srcGeoTiff) as src:
        out_image, out_transform = mask(src, [geoms[i]], crop=True)
    out_meta = src.meta.copy()
    # save the resulting raster
    out_meta.update({"driver": "GTiff", "height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})
    with rasterio.open(targetFolder+"\\"+plotID+".tif", "w", **out_meta) as dest:
        dest.write(out_image)
