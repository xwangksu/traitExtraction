'''
Created on Oct 22, 2018

@author: xuwang
'''
# import csv
import argparse
import pandas
import numpy as np
# from scipy import stats

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFile", required=True,
    help="source file")
#==============
args = ap.parse_args()
sourceFile = args.srcFile

# targetFile = sourceFile.replace('.csv','_s.csv')

dfTrait = pandas.read_csv(sourceFile)

dfPlotCount = dfTrait.groupby("Plot_ID").size()
print(int(np.round(np.mean(dfPlotCount))))

# dfPlotCount.to_csv(targetFile,sep=',',index=False)