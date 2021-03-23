import pandas as pd
import numpy as np
import csv
import ntpath
import simplekml
import os
import sys



#Read file path from command line
fn = sys.argv[1]
if os.path.exists(fn):
    path_to_file = os.path.abspath(fn)
    filename = os.path.basename(fn)
    directory = path_to_file[:-len(filename)]
    filename = filename[:-4]
    #print(path_to_file)
else:
	print("Please put the path to the file as an argument")
#print("*****")
#print(path_to_file)
#print(filename)
#print(directory)

file = pd.read_csv(path_to_file, header=1, delimiter=";", index_col=0)



#Process *************************************************************************************************

#Add empty column

empt = np.zeros(len(file["Location"])).astype(str)
empt[:] = ""
file["Empty0"] = empt
file["Empty1"] = empt
file["Empty2"] = empt


#Add Location for Planet
loc_planet = np.zeros(len(file["Location"])).astype(str)
for i in range(len(file["Location"])):
    
    if file["Location"][i] == "Longyearbyen (LYR)":
        loc_planet[i] = "LYR"
        
    elif file["Location"][i] == "Ny-Alesund":
        loc_planet[i] = "NY"

    elif str(file["Location"][i]) == 'nan':
        loc_planet[i] = "W" + str(file.index[i])
        
    elif isinstance(file["Location"][i], int):
        loc_planet[i] = "W" + str(file["Location"][i])
        
    else:
        loc_planet[i] = str(file["Location"][i])
        
file["LocPlanet"] = loc_planet

#Add column with Lat and Lon together
lat_lon = np.zeros(len(file["Location"])).astype(str)
for i in range(len(lat_lon)):
    lat_lon[i] = '"' + str(file["Lon (+-180)"][i])[:7]+',' + str(file["Lat (+-90)"][i])[:7]+'"'
    
file["LonLat"] = lat_lon




#Save everything to planet csv *****************************************************************************
with open(directory + filename + '_planet.csv', 'w') as the_file:
    for i in range(len(file.index)):
        the_file.write('"Point";' + '"'+file["LocPlanet"][i] + '"' + ';;"red";;;' +  file["LonLat"][i]  +'\n')
        
    the_file.write('"LineString";"";"";"blue";"";"";')
    for i in range(len(file.index)):
        if i < len(file.index)-1:
            the_file.write(file["LonLat"][i] + ';')
        else:
            the_file.write(file["LonLat"][i])

print("Planet file created: " + directory + filename + '_planet.csv')

#Save track to kml *****************************************************************************************
#inputfile = csv.reader(open('foo.csv','r'))
kml=simplekml.Kml()
ls = kml.newlinestring(name=filename)

#inputfile.next(); # skip CSV header
for row in range(len(file.index)):
        ls.coords.addcoordinates([(file["Lon (+-180)"][row],file["Lat (+-90)"][row])]);
        
        pnt = kml.newpoint(name=file["LocPlanet"][row], coords=[(file["Lon (+-180)"][row],file["Lat (+-90)"][row])])
        
        if file["LocPlanet"][row] == "LYR":
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal3/icon56.png'
        
        elif file["LocPlanet"][row] == "NY":
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal3/icon29.png'
            
        else:
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal4/icon49.png'
        #print(ls.coords)
kml.save(directory + filename+'.kml');

print("kml file created: " + directory + filename+'.kml')


#Save track to txt file ************************************************************************************
ex_file = pd.DataFrame(file.index).astype(int)
ex_file["Lat"] = file["Lat (+-90)"].values
ex_file["Lon"] = file["Lon (+-180)"].values
ex_file["FL"] = file["Flightlevel"].values
ex_file["Press"] = file["Pressure (hPa)"].values
ex_file["Dist."] = file["Leg dist. (km)"].values
ex_file["Cum dist."] = file["Cum. dist. (km)"].values
np.savetxt(directory +filename+'.txt', ex_file, fmt='%d %5.2f %5.2f %5.2f %5.2f %5.2f %5.2f', delimiter = ",",header="Lat   Lon   FL    Press   Dist.   Cum. dist")
print("txt file created: " + directory + filename+'.txt')


#Save track to excel file************************************************************************************
def dd2dms(deg):
     d = int(deg)
     md = abs(deg - d) * 60
     m = int(md)
     sd = (md - m) * 60
     
     return str(d)+"° "+str(m)+"' "+str("{:6.3f}".format(sd))+"''"
     #return [d, m, sd]
    
    
excel = file.iloc[:,:7]

dms_lat = np.zeros(len(file.index)).astype(str)
dms_lon = np.zeros(len(file.index)).astype(str)
for i in range(len(dms_lat)):
    dms_lat[i] = dd2dms(file["Lat (+-90)"].values[i]) + " N"
    dms_lon[i] = dd2dms(file["Lon (+-180)"].values[i]) + " E"

excel["dms lat"] = dms_lat
excel["dms lon"] = dms_lon


excel.to_excel(directory +filename+".xlsx")

print("Excel file created: " + directory + filename+'.xlsx')
print("DONE!")
