'''
Created on Oct 17, 2018

@author: xuwang
'''
import argparse
import os
import numpy as np
import rasterio
import csv
#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFolder", required=True,
    help="source images")
#==============
ap.add_argument("-t", "--targetFolder", required=True,
    help="target folder")
#==============
args = ap.parse_args()
filePath = args.srcFolder
targetPath = args.targetFolder
finalFile = open(targetPath+"\\omPixelCTByPlot.csv", 'wt')
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
    writer.writerow(('Plot_ID','Median','Mode'))
    for im in imList:
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imFileName = str(imObj[numOfObj-1])
        plotID = imFileName.split(".tif")[0]
        imageRaw = rasterio.open(im)
        imNpArray = imageRaw.read(1)
        imNpArray[imNpArray<0]=0
        if np.count_nonzero(imNpArray)>0:
#             imNzArray = imNpArray[imNpArray!=0]
#             imFlatNzArray = imNpArray.flatten()
            imNzArray = imNpArray[np.nonzero(imNpArray)]
            # plt.hist(imFlatNzArray,bins=20,range=(0.5,1),edgecolor='black')
            # plt.show()
            bn = int((imNzArray.max()-imNzArray.min())/2)
            hist, bin_edges = np.histogram(imNzArray, bins=bn, density=False)
            # print(imFlatNzArray)
            medianFlat = np.median(imNzArray)
            # print("mean_flat:", meanFlat)
            # medianFlat = np.median(imFlatNzArray)
            # print("median_flat:", medianFlat)
            modeFlat = bin_edges[np.argmax(hist)+1]
            # print("mode_flat:", bin_edges[np.argmax(hist)+1])
            writer.writerow((plotID,'{:.0f}'.format(medianFlat),'{:.0f}'.format(modeFlat)))
finally:
    finalFile.close()