# MSScsv_to_PLANETcsv

This routine transforms an existing MSS csv file into a csv file with the endfix "*_planet.csv", which can be uploaded to the PLANET system. You might have to install the module "simplekml". Do that with the command:

```pip install simplekml```

In addition, several other files are produced:
- a kml file, which can be shown in Google Earth or Windy,
- a txt file (including latitude and longitude in degree+minutes)
- an Excel file (including latitude and longitude in degree+minutes)
- a gpx file.

Executing the program by typing: 

```python MSScsv_to_PLANETcsv.py /path_to_MSS_csv_file/MSS_file.csv```

The program will produce the following files:
```MSS_file_planet.csv```,  ```MSS_file.kml```,```MSS_file.txt```,```MSS_file.xlsx``` and ```MSS_file.gpx```
