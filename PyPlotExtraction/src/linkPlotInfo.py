'''
Created on Oct 17, 2018

@author: xuwang
'''
import csv
import argparse
import pandas

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFile", required=True,
    help="source file")
#==============
ap.add_argument("-i", "--plotInfo", required=True,
    help="plot file")
#==============
args = ap.parse_args()
sourceFile = args.srcFile
plotInfoFile = args.plotInfo
finalFile = sourceFile.replace(".csv","_info.csv")

dfTrait = pandas.read_csv(sourceFile)
dfPlot = pandas.read_csv(plotInfoFile)
# print(dfTrait)

dfFull = dfTrait.merge(dfPlot, left_on='Plot_ID', right_on='Plot_ID', how='left')
# print(dfFull[0])
dfFull.to_csv(finalFile,sep=',',index=False)
