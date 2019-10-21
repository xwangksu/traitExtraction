'''
Created on Oct 17, 2018

@author: xuwang
'''
import argparse
import os
import numpy as np
import rasterio
import cv2
import matplotlib.pyplot as plt
# from tempExtraction import imageFileName
#------------------------------------------------------------------------
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFolder", required=True,
    help="source images")
#==============
args = ap.parse_args()
filePath = args.srcFolder
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
    fileNames=[]
    gcCount=[]
    dpColors=['b','c','y','g','m','k']
    ts_min_old='aa'
    ts_min_num=0
    dpColorFinal = []
    for im in imList:
        # imNum += 1
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imageFileName = str(imObj[numOfObj-1])
        if imageFileName.find('_1_r') != -1:
            ts = imageFileName.split("_")[1]
            ts_min = ts[2:4]
            # print(ts_min)
            if ts_min_old != ts_min:
                ts_min_old = ts_min
                ts_min_num += 1
            dpColorFinal.append(dpColors[ts_min_num-1])
        else:
            dpColorFinal.append('r')
            ts = 'o.m.'
        plotID = '19BYD20206'
        imageRaw = rasterio.open(im)
        imNpArray = imageRaw.read(1)
        imNpArray[imNpArray<0]=0
        # image process
        imgFile = cv2.imread(im)
        th1, canopyArea = cv2.threshold(imgFile, 60, 90, cv2.THRESH_BINARY)
        fileNames.append(ts)
        # print(np.shape(canopyArea))
        gcCount.append(np.count_nonzero(canopyArea)/np.count_nonzero(imgFile))

    # print(dpColorFinal)
    y_pos = np.arange(len(fileNames))
    plt.bar(y_pos, gcCount, align='center', color=dpColorFinal, alpha=0.5)
    plt.xticks(y_pos, fileNames,fontsize=8, rotation=90)
    plt.ylabel('Ground Cover Rate')
    plt.ylim(0, 1)
    plt.title('Ground Coverage of '+plotID+', 2018/11/03') 
    plt.show()
finally:
    print('done')