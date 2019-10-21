'''
Created on Jan 28, 2019

@author: xuwang
'''
import pandas as pd
# import os
import argparse
# import csv
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--srcFile", required=True,
    help="source file")
ap.add_argument("-t", "--tgtFile", required=True,
    help="target file")

args = ap.parse_args()
sourceFile = args.srcFile
targetFile = args.tgtFile
# finalFile = open(targetFile,'wt')
#------------------------------------------------------------------------
df_1 = pd.read_csv(sourceFile)
ssize = np.min(df_1.Plot_ID.value_counts())
print(df_1.Plot_ID.value_counts())
#------------------------------------------------------------------------
dfRaw = open(sourceFile,'r')
try:
    # writer = csv.writer(tgtFile, delimiter=',', lineterminator='\n')
    lineNum = 0
    rLineSet=[]
    nzSet=[]
    snzSet=[]
    for rLine in dfRaw:
        if lineNum != 0:
            rCt=rLine.split(',')
            nz = rCt[9] # vertical angle
            pid = rCt[0]
            if lineNum == 1:
                old_pid = pid
                rLineSet.append(rLine)
                nzSet.append(nz)
                snzSet.append(nz)
            else:
                if pid == old_pid:
                    rLineSet.append(rLine)
                    nzSet.append(nz)
                    snzSet.append(nz)
                else:
                    old_pid = pid
                    # sort the list
                    # sortnzSet = nzSet
                    snzSet.sort(reverse=True)
                    # print(snzSet)
                    # print(nzSet)
                    with open(targetFile, 'a') as fput:
                        if len(snzSet)>=ssize:
                            for j in range(0,ssize):
                                # print(nzSet.index(snzSet[j]))
                                fput.write(rLineSet[nzSet.index(snzSet[j])])
                        else:
                            print(rLineSet[nzSet.index(snzSet[0])])
                            print(len(snzSet))
                    rLineSet = []
                    rLineSet.append(rLine)
                    nzSet = []
                    nzSet.append(nz)
                    snzSet = []
                    snzSet.append(nz)
        else:
            with open(targetFile, 'a') as fput:
                fput.write(rLine)
        lineNum += 1
finally:
    fput.close()