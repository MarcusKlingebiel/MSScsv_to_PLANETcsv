# MSScsv_to_PLANETcsv

This routine transforms an existing MSS csv file into a csv file with the endfix "*_planet.csv", which can be uploaded to the PLANET system. 

In addition, several other files are produced:
- a kml file, which can be shown in Google Earth or Windy,
- a txt file (including latitude and longitude in degree+minutes)
- an Excel file (including latitude and longitude in degree+minutes)
- a gpx file.

Executing the program by typing: 

```python MSScsv_to_PLANETcsv.py /path_to_MSS_csv_file/MSS_file.csv```

The program will produce the following files:
```MSS_file_planet.csv``` and ```MSS_file.kml```
