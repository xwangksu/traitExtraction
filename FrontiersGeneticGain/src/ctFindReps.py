'''
Created on Aug 30, 2018

@author: xuwang
'''
import csv
srcFile='F:/2019_Frontiers/CT_18Ash_BioSorghum/20180919/ctByPlot_final.csv'
dfRaw = open(srcFile,'r')
tgtFile = open('F:/2019_Frontiers/CT_18Ash_BioSorghum/20180919/ctByPlot_wPlot_Info.csv','wt')
try:
    writer = csv.writer(tgtFile, delimiter=',', lineterminator='\n')
    # writer.writerow(('Entry','Row_Column','Reps','nzPixel','Image_File','Temperature-C'))
    # writer.writerow(('Entry','Row_Column','Reps','Mean','Mode'))
    # writer.writerow(('Entry','Row_Column','Reps','nzPixel','Temperature-C'))
    lineNum = 0
    rep = 1
    for rLine in dfRaw:
        rLine = rLine.split("\n")[0]
        if lineNum == 0:
            writer.writerow((rLine,'Entry','Reps'))
        else:
            rCt=rLine.split(',')
            entry = rCt[0].split("$")[0]
            r_c = "$"+ rCt[3]+"$"+rCt[4]
    #         img = rCt[2]
    #         nz = rCt[3]
    #         temp1 = rCt[2]
    #         temp2 = rCt[3].rstrip("\n")
            temp1 = rCt[1]
            temp2 = rCt[2]
            # print(temp)
            if lineNum == 1:
                old_entry = entry
                old_rc = r_c
                rep = 1
            else:
                if entry == old_entry:
                    if r_c != old_rc:
                        rep += 1
                        old_rc = r_c
                else:
                    old_entry = entry
                    old_rc = r_c
                    rep = 1
            # writer.writerow((entry,r_c,rep,nz,img,temp))
            writer.writerow((rLine,entry,rep))
        # writer.writerow((entry,r_c,rep,temp))
        lineNum += 1        
finally:
    tgtFile.close()