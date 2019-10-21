'''
Created on Jan 8, 2019

@author: xuwang
'''
import argparse
import rasterio
import numpy as np
import cv2
import os
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFolder", required=True,
    help="source raster files folder")
ap.add_argument("-tf", "--targetFolder", required=True,
    help="target folder")
args = ap.parse_args()
filePath = args.srcFolder
targetPath = args.targetFolder

exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(name)
print("Total images in the folder: %d" % len(imList))

for im in imList:
    imgFile = rasterio.open(os.path.join(filePath, im))
    r = imgFile.read(1) / 255.0
    g = imgFile.read(2) / 255.0
    b = imgFile.read(3) / 255.0
    
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    v = maxc
    
    deltac = maxc - minc
    s = deltac / maxc
    deltac[deltac == 0] = 1  # to not divide by zero (those results in any way would be overridden in next lines)
    rc = (maxc - r) / deltac
    gc = (maxc - g) / deltac
    bc = (maxc - b) / deltac
    
    h = 4.0 + gc - rc
    h[g == maxc] = 2.0 + rc[g == maxc] - bc[g == maxc]
    h[r == maxc] = bc[r == maxc] - gc[r == maxc]
    h[minc == maxc] = 0.0

    h = (h / 6.0) % 1.0
    h = h * 255
    
    # res = np.dstack([h, s, v])
    cv2.imwrite(os.path.join(targetPath, im), h)

