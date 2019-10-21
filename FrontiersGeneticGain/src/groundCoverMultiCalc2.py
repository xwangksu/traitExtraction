'''
Created on Jan 11, 2019

@author: xuwang
'''
import argparse
import numpy as np
import cv2
import os
import csv
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-sf", "--srcFolder", required=True,
    help="source raster files folder")
ap.add_argument("-tf", "--targetFolder", required=True,
    help="target folder")
args = ap.parse_args()
filePath = args.srcFolder
targetPath = args.targetFolder
#------------------------------------------------------------------------
# Get image file names to process
exten = '.tif'
imList=[]
for dirpath, dirnames, files in os.walk(filePath):
    for name in files:
        if name.lower().endswith(exten):
            imList.append(name)
print("Total images in the folder: %d" % len(imList))
finalFile = open(os.path.join(targetPath, "GroundCover_op.csv"),'wt')
try:
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    # Header row if needed
    writer.writerow(('Plot_ID','Ground_Cover','Original_file'))
    for im in imList:
        pid = str(im).split('-20190')[0]
        imgFile = cv2.imread(os.path.join(filePath, im))
        th1, canopyArea = cv2.threshold(imgFile, 45, 90, cv2.THRESH_BINARY)
        groundCover = np.count_nonzero(canopyArea)
        ofName = '20190' + str(im).split('-20190')[1]
        # ofName = str(ofName).split('-')[1]
        originalFile = ofName.replace('_rgb.tif', '.tif')
        # Save output file
        writer.writerow((pid, groundCover, originalFile))
finally:
    finalFile.close() 