# VisualAids
Improved management of production hardware resources using Raspberry Pi - Develped with Python/Bash Scripting

This project is already implemented on a plant in Mexico.

This project is used for a Tesis for computer science in the UACJ.



---------------------------------------------------------------------------------------------------------------

Visual Aids Script

Instalations needed:
	sudo apt-get install python-pyodbc
	sudo apt-get install unixodbc unixodbc-dev freetds-dev tdsodbc
	sudo apt-get install python-pip
	pip3 install pyodbc
	sudo apt install libreoffice
	sudo apt install cifs-utils
 	sudo apt-get install python3-tk
	sudo apt-get install xdotool
	
FreeTDS Config:
	sudo nano /etc/freetds/freetds.conf
	1. #SQLServer
	2. [sqlserver]
	3. host = 10.120.10.4
	4. port = 1433
	5. tds version = 7.2
	
	sudo nano /etc/odbcinst.ini
	1. [FreeTDS]
	2. Description = TDS driver (Sybase/MS SQL)
	3. Driver = /usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so
	4. Setup = /usr/lib/arm-linux-gnueabihf/odbc/libtdsS.so
	5. CPTimeout =
	6. CPReuse =
	7. FileUsage = 1

	sudo nano /etc/odbc.ini
	1. [sqlserverdatasource]
	2. Driver = FreeTDS
	3. Description = ODBC connection via FreeTDS
	4. Trace = No
	5. Servername = sqlserver
	6. Database = BeFirst

Mount the server into a local folder:
	sudo mkdir /mnt/share
	sudo mount.cifs //10.120.10.4/befirstdata/pn/aids/1 /mnt/share -o user=bchavarria

Make script files executable:
	sudo chmod +x Bash.sh
	sudo chmod +x VisualAids.py

Make the file starts at boot:
	crontab -e
	@reboot /usr/bin/python3 /home/pi/VisualAids.py >>/home/pi/error.txt 2>&1
