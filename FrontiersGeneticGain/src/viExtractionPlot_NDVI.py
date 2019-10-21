'''
Created on Oct 17, 2018

@author: xuwang
'''
import argparse
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import seaborn as sns
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
    dpColors=['blue','orange','yellow','green','purple','brown','black']
    ts_min_old='00'
    ts_min_num=0
    for im in imList:
        # imNum += 1
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imageFileName = str(imObj[numOfObj-1])
        if imageFileName.find('NDVI') != -1:
            ts = imageFileName.split("_")[1]
            ts_min = ts[2:4]
            # print(ts_min)
            if ts_min_old != ts_min:
                ts_min_old = ts_min
                ts_min_num += 1
        plotID = '18BYD20428'
        imageRaw = rasterio.open(im)
        imNpArray = imageRaw.read(1)
        imNpArray[imNpArray<0]=0
        if np.count_nonzero(imNpArray)>0:
            imNzArray = imNpArray[np.nonzero(imNpArray)]
            if imageFileName.find("NDVI") != -1:
                sns.distplot(imNzArray, hist = False, kde = True,
                             color = dpColors[ts_min_num-1],
                             kde_kws = {'linewidth': 1}, label = ts)
            else:
                sns.distplot(imNzArray, hist = False, kde = True,
                         color = 'red',
                         kde_kws = {'linewidth': 3},
                         label = 'o.m.')
    plt.legend(prop={'size': 10}, title = 'Images')
    plt.title('NDVI Density Plot of '+plotID+', 2018/05/16')
    plt.xlabel('NDVI')
    plt.ylabel('Density')
    plt.show()
    
finally:
    print("done")
