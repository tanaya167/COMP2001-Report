import pyodbc

server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_TLai'
username = 'TLai'
password = 'FaiE451*'

print("Starting the connection test...")

try:
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};DATABASE={database};UID={username};PWD={password};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes"  
    )
    print("Connection successful!")
    connection.close()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"SQLSTATE: {sqlstate}")
    print(f"Error message: {ex.args[1]}")

