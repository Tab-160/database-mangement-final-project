
#


import pyodbc
import fileIO
import config


def runSQL(query):
    """Connects to Access database and runs query on it

    Args:
        query: the query to be run over the database
        
    Returns:
        A list of tuples
    """
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + config.PROJECT_LOCATION + 'ASSETS\\finalProject.accdb;'
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
    print()
    print(testing[0])
    print()
    print(testing[1][1])
