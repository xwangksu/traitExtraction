'''
Created on Aug 8, 2019

@author: xuwang
'''
from rasterstats import zonal_stats
import csv

dateStamp = ['20190422','20190424','20190502','20190510','20190522','20190530']

sPath='F:/2019_KS_Wheat/SPAM/'
viRaster = ['GNDVI','NDRE','NDVI']
bandRaster = ['B','G','R','RE','Nir']
for ds in dateStamp:
    # rasterPath = sPath+ds+"/"
    shapeFile = sPath+ds+'/shapefiles/'+ds+'_RF_SPAM_fieldmap.shp'
    for vi in viRaster:
        finalFile = open(sPath+ds+'_'+vi+".csv",'wt')   
        rasterFile = sPath+ds+'/'+ds+'_'+vi+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = "mean", geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',vi))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID').split("$")[0]
                value = '{0:.3f}'.format(rasterMean[i]['properties'].get('mean'))
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
    for bd in bandRaster:
        finalFile = open(sPath+ds+'_'+bd+".csv",'wt')   
        rasterFile = sPath+ds+'/'+ds+'_'+bd+".tif"
        rasterMean = zonal_stats(shapeFile, rasterFile, stats = "mean", geojson_out=True)
        chtLength = len(rasterMean)
        try:
            writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
            writer.writerow(('Plot_ID',bd))
            for i in range(0,chtLength):
                plotIDs = rasterMean[i]['properties'].get('Plot_ID').split("$")[0]
                value = '{0:.4f}'.format(float(rasterMean[i]['properties'].get('mean'))/65536)
                writer.writerow((plotIDs,value))
        finally:
            finalFile.close()
