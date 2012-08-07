#!/usr/bin/python

from SimpleXMLRPCServer import SimpleXMLRPCServer
import networkx as nx
import arcserver
import arcpy
import time

# Create server
#amp-7vcj3h1-dt
#server = SimpleXMLRPCServer(("0.0.0.0", 8000), )
server = SimpleXMLRPCServer(("164.107.86.141", 8000), )


server.register_introspection_functions()


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


    import os
    
    
    # Get the coordinate ASCII file
    #

    
    # Get the output feature class
    #

    tempextentfile = "C:\\Windows\\temp\\tempextent" + str(int(time.time())) + ".shp"
    
    # Get the template feature class
    #
    template = "D:\\GIS Server Data\\agstats\\Receipts.shp"
    
    try:
       # Create the output feature class
       #
       print os.path.dirname(tempextentfile)
       print os.path.basename(tempextentfile)
       arcpy.CreateFeatureclass_management(os.path.dirname(tempextentfile),
                                           os.path.basename(tempextentfile), 
                                           "Polygon", template)
    
       # Open an insert cursor for the new feature class
       #
       cur = arcpy.InsertCursor(tempextentfile)
    
       # Create an array and point object needed to create features
       #
       lineArray = arcpy.Array()
       pnt = arcpy.Point()

       pnt.ID = 1
    
       # Initialize a variable for keeping track of a feature's ID.
       #
       extentsplit = extent.split(",")
       #Bottom Left
       pnt.X = extentsplit[0]
       pnt.Y = extentsplit[1]
       lineArray.add(pnt)
       #Bottom Right
       pnt.X = extentsplit[2]
       pnt.Y = extentsplit[1]   
       lineArray.add(pnt)
       #Top left
       pnt.X = extentsplit[0]
       pnt.Y = extentsplit[3]   
       lineArray.add(pnt)      
       #Top Right
       pnt.X = extentsplit[2]
       pnt.Y = extentsplit[3]   
       lineArray.add(pnt)

       
       feat = cur.newRow()
       feat.shape = lineArray
       cur.insertRow(feat)
       

       del cur
       return tempextentfile
    except Exception as e:
       print e
       return "error"
    

def calcCroplandData(extent):
    
    # Check out any necessary licenses
    arcpy.CheckOutExtension("spatial")
    print extent
    #extent = "-9099915, 5051882, -9043924, 5037452"
    extentfile = createExtentFile(extent)
    if (extentfile == "error"):
        return "error"

    # Script arguments

    ## Need to update this for the future file place
    
    processingfile = "D:\\GIS Server Data\\cropland\\2011_30m_cdls_projectraster.img"

    #processingfile = "D:\\Python Scripts\\LFSservices\\cropland\\2011_30m_cdls_projectraster.img" # provide a default value if unspecified
    #if Agritourism_google_img == '#' or not Agritourism_google_img:
    

    # Local variables:
    tempfile = "C:\\Windows\\temp\\NASS" + str(int(time.time())) + ".img"
    

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
    
    try:
        finalresults = []
        thedbf = dbf.Dbf(tempfile + ".vat.dbf")
        for row in thedbf:
            temparea = row[4]*90*.000247105381
            finalresults.append([row[5], row[4], temparea])
            #results += str(row)
    except Exception as e:
       print e
       return "error"
    

    arcpy.Delete_management(tempfile, "")
    arcpy.CheckInExtension("spatial")

    return finalresults
    
    #C:\Users\hilbert.34\Downloads\dbfpy-2.2.5.tar\dbfpy-2.2.5\setup.py
    
    

def calcPolygonValues(extentfile, processingFile, attributes):
    import os
    import csv
    



    Output_Feature_Class = "C:\\Windows\\temp\\tempclip" + str(int(time.time())) + ".shp"

    try:

        # Process: Clip
        arcpy.Clip_analysis(processingFile, extentfile, Output_Feature_Class, "")
    
    
        #extract to a temp folder
        
        tempcalc2_txt = "C:\\Windows\\temp\\tempcalc" + str(int(time.time())) + ".csv"
            
        
        # Process: Export Feature Attribute to ASCII
        arcpy.ExportXYv_stats(Output_Feature_Class, "NAME;" + attributes, "COMMA", tempcalc2_txt)
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
        
    return resultobj





def calcMeanRaster(extent, thefile):
        

    # Check out any necessary licenses
    arcpy.CheckOutExtension("spatial")

    # Script arguments

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "Agritourism_google.img"

    # Local variables:
    tempfile = "D:\\GIS Server Data\\datafiles\\tempfile" + str(time.time()) + ".img"

    try:
        # Process: Extract by Rectangle
        arcpy.gp.ExtractByRectangle_sa(thefile, extent, tempfile, "INSIDE")
    
        # Process: Get Raster Properties
        meanRes = arcpy.GetRasterProperties_management(tempfile, "MEAN")
    
        arcpy.Delete_management(tempfile, "")
    except Exception as e:
        print e
        return "error"        

    arcpy.CheckInExtension("spatial")
    

    return meanRes.getOutput(0)
    


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
        extentsplit = extent.split(",")
        extent = " ".join([extentsplit[0], extentsplit[3], extentsplit[2], extentsplit[1]])
        WORKINGDIRECTORY = "D:/GIS Server Data/datafiles/"
        processingfiles = ["Agritourism_resample", "ahi_resample", "biodigestor_resample", "grapes_resample", "manurespread_resample", "solarsuit_resample", "winsuit_resample"]
        finalresults = []
        for thefile in processingfiles:
            print "Doing " + thefile
            theresult = calcMeanRaster(extent, WORKINGDIRECTORY + thefile + ".img")
            if (theresult == "error" or str(theresult) == "0"):
                return "error"
            finalresults.append([thefile, theresult])
        return finalresults
        
    def getPolygonValues(self,extent):
        #create the extent raster here so it can be pulled from the processes
        print "running the polygon values"
        extentfile = createExtentFile(extent)
        WORKINGDIRECTORY = "D:/GIS Server Data/agstats/"
        processingfiles = [["AnimalSales", "2007Values"], ["AvgAge", "Value_2007"], ["AvgSize", "2007Averag"], ["CropArea", "2007Value"], \
            ["CropSales", "2007Value"], ["Expenses","2007Value"] , ["GainLoss","ratio"], \
            ["operationsbysizet", "a1_10;a10_50;a50_70;a70_100;a100_140;a140_170;a180_219;a220_259;a260_499;a500_1000;a1000___20;a2000_more"], \
            ["Receipts", "2007Value"], ["TotalOperations", "Values2007"]]
        finalresults =   []     
        for thefile in processingfiles:
            theresult = calcPolygonValues(extentfile, WORKINGDIRECTORY + thefile[0] + ".shp", thefile[1])
            if (theresult == "error" or len(theresult) == 0):
                return "error"
            finalresults.append([thefile[0], theresult])
        arcpy.Delete_management(extentfile, "")
        return finalresults

    def getCroplandData(self, extent):
        print "running the cropland stuff"
        return calcCroplandData(extent)


    
server.register_instance(MyFuncs())

print "serving"
print server.system_listMethods()

# Run the server's main loop
server.serve_forever()


