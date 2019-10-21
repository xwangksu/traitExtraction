'''
Created on Oct 10, 2018

@author: xuwang
'''
import argparse
import os
import numpy as np
import rasterio
import errno
import shutil
#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFolder", required=True,
    help="source file folder")
#==============
# ap.add_argument("-t", "--targetFolder", required=True,
#     help="target folder")
#==============
args = ap.parse_args()
sourceFolder = args.srcFolder
# targetPath = args.targetFolder
exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(sourceFolder):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(os.path.join(dirpath, name))
print("Total images in the path: %d" % len(imList))
# Create renamed path
try:
    os.makedirs(sourceFolder+"\\filtered")
    print("Creating filtered directory.")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
#
for im in imList:
    imageRaw = rasterio.open(im)
    npArray = imageRaw.read(1)
    imFile = im.split('\\')
    imFileName = imFile[len(imFile)-1]
    npArray[npArray<0]=0
#     print(np.count_nonzero(npArray))
#     print(npArray.size)
#     print(imageRaw.width*imageRaw.height)
#     print(npArray)
    if np.count_nonzero(npArray)>=(int)(0.8*imageRaw.width*imageRaw.height):
        tgFile = sourceFolder+"\\filtered\\"+imFileName
        newFile = shutil.copy2(im,tgFile)
