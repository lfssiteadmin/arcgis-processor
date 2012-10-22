# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 11:13:30 2012

@author: hilbert.34
"""

#!/usr/bin/python

#helper functions

import networkx as nx
#import arcserver
#import arcpy
import time




import subprocess
import Image
import numpy
import os
from dbfpy import dbf





def createGraph(nodes,edges):
    mygraph = nx.DiGraph()
    for node in nodes:
        mygraph.add_node(node)
    for edge in edges:
        splitedge = edge.split(":")
        mygraph.add_weighted_edges_from([(splitedge[0], splitedge[1], int(splitedge[2]))])
    return mygraph






def calcCroplandData(extent):
    
    extentarray = extent.split(",")
    
    #enter the file name of the cropland data that has been recoded
    #filenamein = 'C:/Users/hilbert.34/Desktop/cropland/croplanddata_gen.tif'
    filenamein = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\cropland\\croplanddata_gen.tif"
    
    #enter youre temp output location
    filenameout = 'C:/Windows/Temp/croplanddata_gen_temp' + str(int(time.time())) + '.tif'
    
    #make sure this is the right location for the GDAL library
    subprocess.call(["C:/GDAL/gdal_translate.exe", "-projwin", extentarray[0], extentarray[1], extentarray[2],extentarray[3], filenamein,filenameout])    
    
    with open(filenameout, mode='rb') as imagefile:
        im = Image.open(imagefile)
        
        imarray = numpy.array(im)
        del im
        imagefile.close()
    os.remove(filenameout)
    

    histo = numpy.histogram(imarray,bins=[0,1,2,3,4])
    datanames = ["Commodity Crops", "Specialty Crops", "Developed Area", "Natural Resources"]
    
    theresults = []
    for dataname, counter in zip(datanames, histo[0]):
        temparea = counter*900*.000247105381
        theresults.append([dataname, str(temparea)])
        #theresults.append([dataname, "soemthing", temparea])
    
    return theresults
        
  
    
    

def calcPolygonValues(extent):
    
    extentarray = extent.split(",")
    
    #enter the file name of the cropland data that has been recoded
    #filenamein = 'C:/Users/hilbert.34/Desktop/cropland/croplanddata_gen.tif'
    filenamein = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\agstats\\AnimalSales.shp"    
    
    #enter youre temp output location
    filenameout = 'C:/Windows/Temp/tempshapes' + str(int(time.time()))
    

    
    #make sure this is the right location for the GDAL library
    subprocess.call(["C:/GDAL/ogr2ogr.exe", "-clipsrc", extentarray[0], extentarray[3], extentarray[2],extentarray[1],filenameout + '.shp',filenamein])    
        
    db = dbf.Dbf(filenameout + ".dbf")
    
    finalresults = []

    for row in db:
        finalresults.append([row[3],row[4]])
    db.close()
    
    fileext = [".dbf", ".prj", ".shp", ".shx"]
    
    for extension in fileext:
        try:
            os.remove(filenameout + extension)
        except:
            print "did not delete ", extension
    
        
    print finalresults
    
    return finalresults
    
    




def calcMeanRaster(extent, filenamein):
    
    
    extentarray = extent.split(",")
    

    
    #enter youre temp output location
    filenameout = 'C:/Windows/Temp/models_' + str(int(time.time())) + '.tif'
    
    #make sure this is the right location for the GDAL library
    subprocess.call(["C:/GDAL/gdal_translate.exe", "-projwin", extentarray[0], extentarray[1], extentarray[2],extentarray[3], filenamein,filenameout])    
    
    with open(filenameout, mode='rb') as imagefile:
        im = Image.open(imagefile)
        
        imarray = numpy.array(im)
        del im
        imagefile.close()
    os.remove(filenameout)
    
    
    return imarray[imarray>0].mean()
    
    
    
    

from twisted.web import xmlrpc, server


class MyFuncs(xmlrpc.XMLRPC):
    allow_none=True
    allowNone=True
    def get_cycles(self, nodes, edges): 


        mygraph = createGraph(nodes, edges)
        
        cycles =  nx.simple_cycles(mygraph)
        print str(cycles)
        #mygraph.clear()
        return cycles
    
    def xmlrpc_getMeanRaster(self, extent):
        print "runnig the mean raster"
        #need to rotate extent
        WORKINGDIRECTORY = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\datafiles\\"

        processingfiles = ["Agritourism_normalize.tif", "ahi_normalize.tif", "biodigestor_normalize.tif", "grapes_google.img", "manurespread_google.img", "solarsuit_normalize.tif", "winsuit_normalize.tif"]
        finalresults = []
        for thefile in processingfiles:
            print "Doing " + thefile
            theresult = calcMeanRaster(extent, WORKINGDIRECTORY + thefile)
            if (theresult == "error" or str(theresult) == "0"):
                return "error"
            finalresults.append([thefile, str(theresult)])
        print finalresults
        return finalresults
        
    def xmlrpc_getPolygonValues(self,extent):
        #create the extent raster here so it can be pulled from the processes
        print "running the polygon values"


        theresult = calcPolygonValues(extent)
        if (theresult == "error" or len(theresult) == 0):
            return "error"

        print theresult
        return theresult

    def xmlrpc_getCroplandData(self, extent):
        print "running the cropland stuff"
        return calcCroplandData(extent)
        
        
        
        
        

import sys

if __name__ == '__main__':
    from twisted.internet import reactor
    r = MyFuncs()
    xmlrpc.addIntrospection(r)
    if (len(sys.argv) > 1 and sys.argv[1] == "test"):
        myobj = reactor.listenTCP(8000, server.Site(r), interface = '164.107.87.183')
    else:
        myobj = reactor.listenTCP(8000, server.Site(r), interface = "164.107.84.29")
    
    print "running"
    reactor.run()        


        
        
        

       
        
        
        
        
        
        
        
        
        
        






