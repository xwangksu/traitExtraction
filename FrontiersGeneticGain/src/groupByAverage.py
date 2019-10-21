'''
Created on Jan 29, 2019

@author: xuwang
'''
import pandas as pd
import argparse
import csv
#------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFile", required=True,
    help="source file")
ap.add_argument("-t", "--tgtFile", required=True,
    help="target file")
#==============
args = ap.parse_args()
sourceFile = args.srcFile
targetFile = args.tgtFile
finalFile = open(targetFile,'wt')
df_1 = pd.read_csv(sourceFile, usecols=[0,1])

res = df_1.groupby(['Plot_ID']).mean()

try:
    # Create final output file
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    writer.writerow(('Plot_ID','GC_average'))
    for i in range(len(res.index)):
        writer.writerow((res.index[i], '{0:.3f}'.format(res.Ground_Cover[i])))
finally:
    finalFile.close()