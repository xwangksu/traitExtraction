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
    for im in imList:
        # imNum += 1
        imObj = im.split("\\")
        numOfObj = len(imObj)
        imFileName = str(imObj[numOfObj-1])
        ts = imFileName.split("_")[1]
        # 0919
        # ts = ts.split(".")[0]
        plotID = "16CS3071-3070$8$4"
        imageRaw = rasterio.open(im)
        imNpArray = imageRaw.read(1)
        imNpArray[imNpArray<0]=0
        if np.count_nonzero(imNpArray)>0:
            imNzArray = imNpArray[np.nonzero(imNpArray)]
            if imFileName.find("or") != -1:
            # 0919
#             if imFileName.find("$$$") != -1:    
                imNpArray = imNpArray*0.04-273.15
            imNpArray[imNpArray<0]=0
            imNzArray = imNpArray[np.nonzero(imNpArray)]
            if imFileName.find("or") != -1:
                if ts.find("1425") != -1:
                    sns.distplot(imNzArray, hist = False, kde = True,
                         color = 'orange',
                         kde_kws = {'linewidth': 1},
                         label = ts)
                else:
                    sns.distplot(imNzArray, hist = False, kde = True,
                         color = 'purple',
                         kde_kws = {'linewidth': 1},
                         label = ts)
            # 0919
#             if imFileName.find("$$$") != -1:
#                 if ts.find("1324") != -1:
#                     sns.distplot(imNzArray, hist = False, kde = True,
#                          color = 'blue',
#                          kde_kws = {'linewidth': 1},
#                          label = ts)
#                 elif ts.find("1325") != -1:
#                     sns.distplot(imNzArray, hist = False, kde = True,
#                          color = 'orange',
#                          kde_kws = {'linewidth': 1},
#                          label = ts)
#                 elif ts.find("1326") != -1:
#                     sns.distplot(imNzArray, hist = False, kde = True,
#                          color = 'yellow',
#                          kde_kws = {'linewidth': 1},
#                          label = ts)
#                 elif ts.find("1327") != -1:
#                     sns.distplot(imNzArray, hist = False, kde = True,
#                          color = 'green',
#                          kde_kws = {'linewidth': 1},
#                          label = ts)
#                 else:
#                     sns.distplot(imNzArray, hist = False, kde = True,
#                          color = 'purple',
#                          kde_kws = {'linewidth': 1},
#                          label = ts)
            else:
                sns.distplot(imNzArray, hist = False, kde = True,
                         color = 'red',
                         kde_kws = {'linewidth': 3},
                         label = 'o.m.')
    plt.legend(prop={'size': 7}, title = 'Images')
    plt.title('CT Density Plot of '+plotID+', 2018/08/25')
    plt.xlabel('Temperature (C)')
    plt.ylabel('Density')
    plt.show()
finally:
    print("done")