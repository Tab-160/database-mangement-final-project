
#


import pyodbc


def runSQL(query):
    """Connects to Access database and runs query on it

    Args:
        query: the query to be run over the database
    """
    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\rgreenup24\\Desktop\\finalProject\\assets\\finalProject.accdb;'
    conn = pyodbc.connect(conn_str)
    crsr = conn.cursor()

    data = ""   # This will be filled with the data
    rows = crsr.execute(query)
    for row in rows:
        data += str(row) + "\n"

    return data

if __name__ == '__main__':
    print(runSQL("Select *\nFrom users"))
