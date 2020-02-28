import pyodbc 
import csv
from dotenv import load_dotenv
import os
load_dotenv()
bearer =  os.environ.get('bearer-token')
connectionString = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=;DATABASE=;UID=;PWD="
query = """
select dbo.Computer_System_DATA.Manufacturer00,dbo.Computer_System_DATA.Model00,dbo.Computer_System_DATA.Name00,dbo.COMPUTER_SYSTEM_PRODUCT_DATA.IdentifyingNumber00,dbo.System_IP_Address_ARR.IP_Addresses0,dbo.System_MAC_Addres_ARR.MAC_Addresses0,dbo.System_DATA.SMSID0,dbo.System_Enclosure_DATA.chassisTypes00
FROM dbo.Computer_System_DATA,
dbo.COMPUTER_SYSTEM_PRODUCT_DATA,
dbo.System_IP_Address_ARR,
dbo.System_MAC_Addres_ARR,
dbo.System_DATA,
dbo.System_Enclosure_DATA
where 
dbo.Computer_System_DATA.MachineID = dbo.COMPUTER_SYSTEM_PRODUCT_DATA.MachineID and dbo.COMPUTER_SYSTEM_PRODUCT_DATA.MachineID = dbo.System_IP_Address_ARR.ItemKey and dbo.System_IP_Address_ARR.ItemKey = dbo.System_MAC_Addres_ARR.ItemKey and dbo.System_MAC_Addres_ARR.ItemKey = dbo.System_DATA.MachineID and  dbo.System_DATA.MachineID = dbo.System_Enclosure_DATA.MachineID
"""
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()
cursor.execute(query)
data = cursor.fetchone()

columns = [column[0] for column in cursor.description]
print(columns)
results = []
for row in cursor.fetchall():
    results.append(dict(zip(columns, row)))

filteredResults = []
for item in results:
    length = len(filteredResults)
    if length == 0:
        filteredResults.append(item)

    elif item['Manufacturer00'] == 'Apple Inc.':
        continue

    elif item['IdentifyingNumber00'] != filteredResults[length-1]['IdentifyingNumber00']:
        filteredResults.append(item)
  

print(filteredResults)
print(len(filteredResults))


csv_columns = ['Manufacturer00', 'Model00', 'Name00', 'IdentifyingNumber00', 'IP_Addresses0', 'MAC_Addresses0', 'SMSID0','chassisTypes00']

csv_file = "Names.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in filteredResults:
            writer.writerow(data)
except IOError:
    print("I/O error")