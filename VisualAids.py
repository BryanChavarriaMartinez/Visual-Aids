#!/usr/bin/python
import pyodbc
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
from time import sleep

sleep(10)

## Globals ##
## Settings for Visual Aids:
# Note: The Station may change depending on where we are going to use the Rasp
StationID = '1' 
## Settings for DB Connection:
DSN = 'sqlserverdatasource'
DB = 'BeFirst'
User = 'DBRasp'
Pass = 'Raspberry741'
## Connection strings:
conn_string = "DSN="+DSN+";UID="+User+";PWD="+Pass+";DATABASE="+DB+";"
## Queries:
url_query = "SELECT VA.PartID, ST.AreaID, VA.url, ST.LastSide, VA.ProcessID, VA.Version FROM EN_tbl_visualAids VA INNER JOIN PD_idt_stations ST ON VA.PartID = ST.LastPartID AND ST.LastSide = VA.Side WHERE ST.StationID = "+StationID+" AND VA.Version = (SELECT MAX(Version) FROM EN_tbl_visualAids VA INNER JOIN PD_idt_stations ST ON ST.LastPartID = VA.PartID AND ST.LastSide = VA.Side WHERE ST.StationID = "+StationID+")"
## End Global ##

## Executes the connection string to the server
def ConnectCursor():
    try:
        conn = pyodbc.connect(conn_string)
        return conn
            
    except Exception as e:
        print(e)
    
## Retrieve values from the DB    
def ValuesFromDB():
    PartID = ''
    AreaID = ''
    ProcessID = ''
    LastSide = ''
    Version = ''
    try:
        conn = ConnectCursor()
        cursor = conn.cursor()
        
        cursor.execute(url_query)
        first_row = cursor.fetchone()
        if (first_row is None):
            FileName = 'Blank'
        else:
            cursor.execute(url_query)
            data = cursor.fetchall()
            for row in data:
                PartID = str(row[0])
                AreaID = str(row[1])
                LastSide = str(row[3])
                ProcessID = str(row[4])
                Version = str(row[5])
                break
            FileName = str(LastSide + "_" + ProcessID + "_" + Version + ".pptx")
    
    except Exception as e:
        print(e)
        
    finally:
        return PartID,AreaID,LastSide,ProcessID,Version,FileName
    
## Write our Bash script that is going to run the Visual Aids
def WriteBash(PartID,AreaID,FileName):
    # ServerFolder = 'smb://10.120.10.4/befirstdata/pn/aids/1'
    # Strings
    Local_Folder = str("/home/pi/Aids/1/" + PartID + "/" + AreaID)
    Local_File = str("/home/pi/Aids/1/" + PartID + "/" + AreaID + "/" + FileName)
    Mount_File = str("/mnt/share/" + PartID + "/" + AreaID + "/" + FileName)
    try:
        # Open our Bash file
        Bash_File = open("Bash.sh","w")
        
        # Start writing on our Bash file
        Bash_File.write("#!/bin/bash \n")
        
        # Check if the Aids > then the Part ID > then Area ID folders are already created
        # (mkdir -p) Create all the directories if those doesnt exist
        if(os.path.isdir(Local_Folder) == False):
            Bash_File.write("sudo mkdir -p "+Local_Folder+" \n")
        # If the file exist we open it with libreoffice.
        # Else, copy the file from the server to our folders previously created
        # And open the file we have just paste in our Rasp
        if(os.path.exists(Local_File) == True):
            Bash_File.write("sudo /usr/bin/libreoffice "+Local_File+" \n")
        else:
            Bash_File.write("sudo cp "+Mount_File+" "+Local_Folder+" \n")
            Bash_File.write("sudo /usr/bin/libreoffice "+Local_File+" \n")
        
        Bash_File.write("xdotool search --onlyvisible --class libreoffice key F5 \n")
        Bash_File.write("while :; do xdotool search --onlyvisible --class libreoffice key Right ; sleep 5; done \n")
        
        Bash_File.write("sleep 30 \n")
        Bash_File.write("python3 ./VisualAids.py \n")
        Bash_File.close()
        
    except Exception as e:
        print(e)
        
## Run the Bash scrit
def RunBash():
    try:
        subprocess.call("./Bash.sh", shell=True)
        
    except Exception as e:
        print(e)
    
## Main ##
if __name__ == "__main__":
    # Get values from DB
    PartID,AreaID,LastSide,ProcessID,Version,FileName = ValuesFromDB()
    
    if(FileName == 'Blank'):
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('No operations','The selected station/process is not active')
    else:
        # Write out Bash File with DB values
        WriteBash(PartID,AreaID,FileName)
        # Run the Bash script
        RunBash()