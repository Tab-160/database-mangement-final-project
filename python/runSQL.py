
#


import pyodbc
import fileIO


def runSQL(query):
    """Connects to Access database and runs query on it

    Args:
        query: the query to be run over the database
        
    Returns:
        A list of tuples
    """
    conn_str = r'DRIVER={Driver do Microsoft Access (*.mdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;DriverId=25;DefaultDir=ASSETS;DBQ=' + fileIO.PROJECT_LOCATION + r'ASSETS\finalProject.mdb;'
    conn = pyodbc.connect(conn_str)
    crsr = conn.cursor()

    data = []   # This will be filled with the data
    rows = crsr.execute(query)
    for row in rows:
        data.append((row))

    return data

if __name__ == '__main__':
    testing = runSQL("SELECT * FROM products")
    print(testing)
    print(testing[0])
    print(testing[1][1])
