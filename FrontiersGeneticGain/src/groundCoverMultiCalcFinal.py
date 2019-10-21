'''
Created on Jan 14, 2019

@author: xuwang
'''
import pandas as pd
import os
import argparse
import csv
import numpy as np
import utm
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFile", required=True,
    help="source file")
ap.add_argument("-t", "--targetPath", required=True,
    help="target path")
ground_ref = 313.2 # ASH BYD2
#==============
args = ap.parse_args()
sourceFile = args.srcFile
tPath = args.targetPath
finalFile = open(os.path.join(tPath, "GroundCoverRate_op_final.csv"),'wt')
#------------------------------------------------------------------------
dfKeep = pd.read_csv(sourceFile, usecols=[0,1,2], dtype=str)
pID = dfKeep['Plot_ID'].values.tolist()
gCover = dfKeep['Ground_Cover'].values.tolist()
imgFile = dfKeep['Original_file'].values.tolist()

dfCoor = pd.read_csv(sourceFile, usecols=[3,4,5,6,7], dtype=np.double)
plot_x = dfCoor['X_Plot'].values.tolist()
plot_y = dfCoor['Y_Plot'].values.tolist()
longi = dfCoor['Longitude'].values.tolist()
lati = dfCoor['Latitude'].values.tolist()
alti = dfCoor['Altitude'].values.tolist()
try:
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    # Header row if needed
    writer.writerow(('Plot_ID','Ground_Cover','H_Distance','V_Distance','H_Degree','V_Degree','Original_file','Plot_Center_Longitude',
                     'Plot_Center_Latitude','Camera_Longitude','Camera_Latitude','Time_Stamp'))
    for i in range(len(pID)):
        [utmPlotX, utmPlotY, latPlotZone, longPlotZone] = utm.from_latlon(plot_y[i],plot_x[i])
        # print(utm.from_latlon(plot_y[i],plot_x[i]))
        [utmCamX, utmCamY, latCamZone, longCamZone] = utm.from_latlon(lati[i],longi[i])
        point_plot = np.array((utmPlotX, utmPlotY))
        point_cam = np.array((utmCamX, utmCamY))
        diffDist = np.sqrt(np.sum((point_plot - point_cam) ** 2))
        vDist = np.abs(alti[i] - ground_ref)
        h_dg = np.arctan2(utmCamY-utmPlotY, utmCamX-utmPlotX) * 180 / np.pi
        v_dg = np.arctan2(diffDist, vDist) * 180 / np.pi
        ts = imgFile[i].split("_")[1]
        writer.writerow((pID[i], '{0:.3f}'.format(np.double(gCover[i])), '{0:.2f}'.format(diffDist), '{0:.2f}'.format(vDist),
                         '{0:.2f}'.format(h_dg), '{0:.2f}'.format(v_dg), imgFile[i],'{0:.8f}'.format(plot_x[i]),'{0:.8f}'.format(plot_y[i]),
                         '{0:.8f}'.format(longi[i]),'{0:.8f}'.format(lati[i]),ts))
finally:
    finalFile.close()
    