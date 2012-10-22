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
import pickle





def createGraph(nodes,edges):
    mygraph = nx.DiGraph()
    for node in nodes:
        mygraph.add_node(node)
    for edge in edges:
        splitedge = edge.split(":")
        mygraph.add_weighted_edges_from([(splitedge[0], splitedge[1], int(splitedge[2]))])
    return mygraph





def createExtentFile(extent):
    # Create a new line feature class using a text file of coordinates.
    #   Each coordinate entry is semicolon delimited in the format of ID;X;Y
    
    # Import ArcPy and other required modules
    
    return "error"


    import os
    
    
    # Get the coordinate ASCII file
    #

    
    # Get the output feature class
    #

    tempextentfile = "C:\\Windows\\temp\\tempextent" + str(int(time.time())) + ".shp"
    
    # Get the template feature class
    #
    template = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\templateprojected.shp"
    
    try:
       # Create the output feature class
       #
       arcpy.CreateFeatureclass_management(os.path.dirname(tempextentfile),
                                           os.path.basename(tempextentfile), 
                                           "Polygon", template, "DISABLED", "DISABLED", template)
    
       # Open an insert cursor for the new feature class
       #
       print "doing cursor"
       cur = arcpy.InsertCursor(tempextentfile)
       print "could not do cursor"
    
       # Create an array and point object needed to create features
       #
       lineArray = arcpy.Array()
       pnt = arcpy.Point()

       pnt.ID = 1
    
       # Initialize a variable for keeping track of a feature's ID.
       #
       print "adding the feature"
       extentsplit = extent.split(",")
       #Bottom Left
       pnt.X = extentsplit[0]
       pnt.Y = extentsplit[1]
       lineArray.add(pnt)
       #Bottom Right
       pnt.X = extentsplit[2]
       pnt.Y = extentsplit[1]   
       lineArray.add(pnt)
       #Top Right
       pnt.X = extentsplit[2]
       pnt.Y = extentsplit[3]   
       lineArray.add(pnt)
       #Top left
       pnt.X = extentsplit[0]
       pnt.Y = extentsplit[3]   
       lineArray.add(pnt)      


       
       feat = cur.newRow()
       feat.shape = lineArray
       cur.insertRow(feat)
       
       print "deleting cursor"
       del cur
       return tempextentfile
    except Exception as e:
       print e
       return "error"
    

def calcCroplandData(extent):
    
    filenamein = 'C:/Users/hilbert.34/Desktop/cropland/croplanddata_gen.tif'
    filenameout = 'C:/Users/hilbert.34/Desktop/cropland/croplanddata_gen_temp' + str(int(time.time())) + '.tif'
    
    ps = subprocess.call(["C:/GDAL/gdal_translate.exe", "-projwin", "-9578185", "4622715", "-9506803","4580583", filenamein,filenameout])    
    print "writing now"    
    
    finalresults = []   
    
    with open(filenameout, mode='rb') as imagefile:
        im = Image.open(imagefile)
        
        print "image closed"
        imarray = numpy.array(im)
        del im
        print "got array"
        imagefile.close()
    print "file removed"
    os.remove(filenameout)

    print "converted to array"
    histo = numpy.histogram(imarray,bins=[0,1,2,3,4])
    datanames = ["Commodity Crops", "Specialty Crops", "Developed Area", "Natural Resources"]

    for dataname, counter in zip(datanames, histo[0]):
        temparea = counter*900*.000247105381
        finalresults.append([dataname, " ", temparea])
    print finalresults

    return pickle.dumps(finalresults)

    return finalresults
    
  
      
    
    
#            if row[0] == 0: 
#                dataname = "Commodity Crops"
#            elif row[0] == 1: 
#                dataname = "Specialty Crops"
#            elif row[0] == 2: 
#                dataname = "Developed Area"
#            elif row[0] == 3: 
#                dataname = "Natural Resources"    
    
    
    #### OLD CODE
    
    
    
    
    # Check out any necessary licenses
    arcpy.CheckOutExtension("spatial")
    #extent = "-9099915, 5051882, -9043924, 5037452"
    extentfile = createExtentFile(extent)
    if (extentfile == "error"):
        return "error"
        
        
        
        

    # Script arguments

    ## Need to update this for the future file place
    
    processingfile = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\cropland\\croplanddata_gen.tif"

    #processingfile = "D:\\Python Scripts\\LFSservices\\cropland\\2011_30m_cdls_projectraster.img" # provide a default value if unspecified
    #if Agritourism_google_img == '#' or not Agritourism_google_img:
    

    # Local variables:
    tempfile = "C:\\Windows\\temp\\NASS" + str(int(time.time())) + ".img"
    
    print "extracting mask"
    # Process: Extract by Rectangle
    #arcpy.gp.ExtractByRectangle_sa(processingfile, extent, tempfile, "INSIDE")
    #print "finished extracting"
    try:
        outExtractByMask = arcpy.sa.ExtractByMask(processingfile, extentfile)
        outExtractByMask.save(tempfile)
        arcpy.Delete_management(extentfile, "")
    except Exception as e:
        print e
        return "error"
    #results = ""
    from dbfpy import dbf
    
    #on the new 0 -     
    
    try:
        finalresults = []
        thedbf = dbf.Dbf(tempfile + ".vat.dbf")
        for row in thedbf:
            dataname = ""
            if row[0] == 0: 
                dataname = "Commodity Crops"
            elif row[0] == 1: 
                dataname = "Specialty Crops"
            elif row[0] == 2: 
                dataname = "Developed Area"
            elif row[0] == 3: 
                dataname = "Natural Resources"
            else :
                dataname = "Misc"
            temparea = row[1]*900*.000247105381
            finalresults.append([dataname, row[1], temparea])
            #results += str(row)
    except Exception as e:
       print e
       return "error"
    

    arcpy.Delete_management(tempfile, "")
    arcpy.CheckInExtension("spatial")

    return finalresults
    
    #C:\Users\hilbert.34\Downloads\dbfpy-2.2.5.tar\dbfpy-2.2.5\setup.py
    
    

def calcPolygonValues(extentfile, processingFile):
    
    return "error"    
    
    import os
    import csv
    



    Output_Feature_Class = "C:\\Windows\\temp\\tempclip" + str(int(time.time())) + ".shp"

    try:

        # Process: Clip
        arcpy.Clip_analysis(processingFile, extentfile, Output_Feature_Class, "")
    
    
        #extract to a temp folder
        
        tempcalc2_txt = "C:\\Windows\\temp\\tempcalc" + str(int(time.time())) + ".csv"
            
        
        #Process: Export Feature Attribute to ASCII
        arcpy.ExportXYv_stats(Output_Feature_Class, "CNTYIDFP;NAME", "COMMA", tempcalc2_txt)
        arcpy.Delete_management(Output_Feature_Class, "")
        resultfile = open(tempcalc2_txt, 'rb')
        resultreader = csv.reader(resultfile)
        resultobj = []
        for row in resultreader:
            resultobj.append(row[2:len(row)])
        resultfile.close()   
        os.remove(tempcalc2_txt)
    
    except Exception as e:
        print e
        return "error"
    print resultobj
    return resultobj





def calcMeanRaster(extentfile, thefile):
    
    return "error"
        

    # Check out any necessary licenses
    arcpy.CheckOutExtension("spatial")

    # Script arguments

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Agritourism_google.img"

    # Local variables:
    tempfile = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\datafiles\\tempfile" + str(int(time.time())) + ".img"

    try:
        outExtractByMask = arcpy.sa.ExtractByMask(thefile, extentfile)
        outExtractByMask.save(tempfile)
        # Process: Extract by Rectangle
        #arcpy.gp.ExtractByRectangle_sa(thefile, extent, tempfile, "INSIDE")
    
        # Process: Get Raster Properties
        meanRes = arcpy.GetRasterProperties_management(tempfile, "MEAN")
    
        arcpy.Delete_management(tempfile, "")
    except Exception as e:
        print e
        return "error"        

    arcpy.CheckInExtension("spatial")
    

    return meanRes.getOutput(0)
    













#start this with server.py test

import SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):pass


class MyFuncs:
    def get_cycles(self, nodes, edges): 


        mygraph = createGraph(nodes, edges)
        
        cycles =  nx.simple_cycles(mygraph)
        print str(cycles)
        #mygraph.clear()
        return cycles
    
    def getMeanRaster(self, extent):
        print "runnig the mean raster"
        #need to rotate extent
        WORKINGDIRECTORY = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\datafiles\\"
        extentfile = createExtentFile(extent)
        if (extentfile == "error"):
            return "error"
        processingfiles = ["Agritourism_resample", "ahi_resample", "biodigestor_resample", "grapes_resample", "manurespread_resample", "solarsuit_resample", "winsuit_resample"]
        finalresults = []
        for thefile in processingfiles:
            print "Doing " + thefile
            theresult = calcMeanRaster(extentfile, WORKINGDIRECTORY + thefile + ".img")
            if (theresult == "error" or str(theresult) == "0"):
                return "error"
            finalresults.append([thefile, theresult])
        arcpy.Delete_management(extentfile, "")
        return finalresults
        
    def getPolygonValues(self,extent):
        #create the extent raster here so it can be pulled from the processes
        print "running the polygon values"
        extentfile = createExtentFile(extent)
        WORKINGDIRECTORY = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\agstats\\"
        processingfiles = [["AnimalSales"]]
        #THE OPERTIONS VALUES  are in a10_50	a100_140	a140_170	a180_219	a2000_more	a220_259	a260_499	a50_70	a500_1000	a70_100
            #, "2007Values"
#        , ["AvgAge", "Value_2007"], ["AvgSize", "2007Averag"], ["CropArea", "2007Value"], \
#            ["CropSales", "2007Value"], ["Expenses","2007Value"] , ["GainLoss","ratio"], \
#            ["operationsbysizet", "a1_10;a10_50;a50_70;a70_100;a100_140;a140_170;a180_219;a220_259;a260_499;a500_1000;a1000___20;a2000_more"], \
#            ["Receipts", "2007Value"], ["TotalOperations", "Values2007"]]
        finalresults =   []     
        for thefile in processingfiles:
            theresult = calcPolygonValues(extentfile, WORKINGDIRECTORY + thefile[0] + ".shp")
            if (theresult == "error" or len(theresult) == 0):
                return "error"
            finalresults.append([thefile[0], theresult])
        arcpy.Delete_management(extentfile, "")
        print finalresults
        return finalresults

    def getCroplandData(self, extent):
        print "running the cropland stuff"
        return calcCroplandData(extent)
        
        
        
import sys        
        
# Create server
#amp-7vcj3h1-dt
#server = SimpleXMLRPCServer(("0.0.0.0", 8000), )

if (len(sys.argv) > 1 and sys.argv[1] == "test"):
    server = AsyncXMLRPCServer(("164.107.87.183", 8000), SimpleXMLRPCRequestHandler, allow_none=True)
    print "running as test server"     
else:
    server = AsyncXMLRPCServer(("164.107.84.29", 8000), SimpleXMLRPCRequestHandler, allow_none=True) 
    THEPATH = "\\\\it-bitbox-vm\\share\\AMP\\GIS Server Data\\"


server.register_instance(MyFuncs())


server.register_introspection_functions()        

print "serving"
print server.system_listMethods()

# Run the server's main loop
server.serve_forever()
       
        
        
        
        
        
        
        
        
        
        






