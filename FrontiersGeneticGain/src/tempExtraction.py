'''
Created on Aug 29, 2018

@author: xuwang
'''
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
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
finalFile = open(targetPath+"\\tempImagePlot.csv", 'wt')
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
    # imNum = 0
    for im in imList:
        # imNum += 1
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imFileName = str(imObj[numOfObj-1])
        imElement = imFileName.split("-")
        imageFileName = imElement[len(imElement)-1]
        pID = imElement[0]+"-"+imElement[1]+"-"+imElement[2]+"-"+imElement[3]+"-"+imElement[4]
        imageRaw = plt.imread(im)
        if np.count_nonzero(imageRaw)>0:
            # mean_temp = np.sum(imageRaw)/np.count_nonzero(imageRaw)*0.04-273.15
            temp = imageRaw <= 60
            mean_temp = np.sum(imageRaw[temp])/len(imageRaw[temp])
            writer.writerow((pID, '{0:.3f}'.format(mean_temp), imageFileName))
finally:
    finalFile.close()