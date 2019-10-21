'''
Created on Jan 14, 2019

@author: xuwang
'''
import argparse
import pandas
import os

ap = argparse.ArgumentParser()
ap.add_argument("-vi", "--viFile", required=True,
    help="ground cover orthophoto file")
ap.add_argument("-pc", "--plotCoord", required=True,
    help="plot coordinate file")
ap.add_argument("-oc", "--orthoCoord", required=True,
    help="orthophoto coordinate file")
ap.add_argument("-tp", "--targetPath", required=True,
    help="target path")
args = ap.parse_args()
gcFile = args.viFile
pcFile = args.plotCoord
ocFile = args.orthoCoord
tPath  = args.targetPath

finalFile = open(os.path.join(tPath, "viByPlot_2.csv"),'wt')
dfTrait = pandas.read_csv(gcFile)
dfPlot = pandas.read_csv(pcFile)
dfImage = pandas.read_csv(ocFile)
dfTraitPlot = dfTrait.merge(dfPlot, left_on='Plot_ID', right_on='Plot_ID', how='left')
dfFinal = dfTraitPlot.merge(dfImage, left_on='Original_file', right_on='Original_file', how='left')
dfFinal.to_csv(finalFile, sep=',', index=False)