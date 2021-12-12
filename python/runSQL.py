"""Everything about running SQL commands is stored here

    Currently, this only has runSQL on /assets/finalProject.mdb
    Methods:
        runSQL(query)

"""

import pyodbc
import fileIO

def runSQL(query):
    """Connects to Access database and runs query on it

    Args:
        query: string with the query to be run over the database
        
    Returns:
        A list of tuples
    """
    # See documentation for more details
    conn_str = r"DRIVER={Driver do Microsoft Access (*.mdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;DriverId=25;DefaultDir=" + fileIO.PROJECT_LOCATION + "ASSETS;DBQ=" + fileIO.PROJECT_LOCATION + "ASSETS\\finalProject.mdb;"
    conn = pyodbc.connect(conn_str)
    crsr = conn.cursor()

    data = []   # Store data as an array
    # Run SQL, store in data
    rows = crsr.execute(query)
    for row in rows:
        data.append((row))

    return data

