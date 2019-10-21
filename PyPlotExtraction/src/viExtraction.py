'''
Created on Oct 17, 2018

@author: xuwang
'''
import argparse
import os
import numpy as np
import rasterio
import csv
# import matplotlib.pyplot as plt
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
finalFile = open(targetPath+"\\viByPlot.csv", 'wt')
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
    writer.writerow(('Plot_ID','Range','Column','Original_file','Mean','Mode','NonZeroCount'))
    # imNum = 0
    for im in imList:
        # imNum += 1
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imFileName = str(imObj[numOfObj-1])
        imElement = imFileName.split("-")
        numOfImElement = len(imElement)
        pID = imElement[0]
        if pID.find("$$$") != -1:
            pID = pID.replace("$$$","/")
        pElement = pID.split("$")
        plotID = pElement[0]
        rangeNum = pElement[1]
        columNum = pElement[2]
        imageFileName = imElement[numOfImElement-1]
#         imageFile = imElement[0].split("\\")
#         imageFileName = imageFile[len(imageFile)-1]
#         pID = imElement[1].replace(".tif","")
#         if pID.find("$$$") != -1:
#             pID.replace("$$$","/")
        imageRaw = rasterio.open(im)
        imNpArray = imageRaw.read(1)
        imNpArray[imNpArray<0]=0
        if np.count_nonzero(imNpArray)>0:
            # print(np.sum(imageRaw)/np.count_nonzero(imageRaw))
            # print(np.sum(imageRaw))
            # mean_vi = np.sum(imNpArray)/np.count_nonzero(imNpArray)
#             imNzArray = imNpArray[imNpArray!=0]
#             imFlatNzArray = imNpArray.flatten()
            imNzArray = imNpArray[np.nonzero(imNpArray)]
            # imFlatNzArray = imNpArray.flatten()
#             print(np.count_nonzero(imNzArray))
#             print(len(imNzArray))
#             plt.hist(imNzArray,bins=10,edgecolor='black')
#             plt.show()
            hist, bin_edges = np.histogram(imNzArray, bins=10, density=False)
            # print(imFlatNzArray)
            meanFlat = np.mean(imNzArray)*0.04-273.15
            # print("mean_flat:", meanFlat)
            # medianFlat = np.median(imFlatNzArray)
            # print("median_flat:", medianFlat)
            modeFlat = bin_edges[np.argmax(hist)+1]*0.04-273.15
            # writer.writerow((plotID,rangeNum,columNum,imageFileName.replace("_NDVI.tif","_1.tif"),'{:.3f}'.format(meanFlat),'{:.3f}'.format(modeFlat),np.count_nonzero(imNpArray)))
            writer.writerow((plotID+"$"+rangeNum+"$"+columNum,rangeNum,columNum,imageFileName,'{:.3f}'.format(meanFlat),'{:.3f}'.format(modeFlat),np.count_nonzero(imNpArray)))
finally:
    finalFile.close()