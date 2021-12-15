"""Everything about running SQL commands is stored here

    Currently, this only has runSQL on /assets/finalProject.mdb
    Methods:
        runSQL(query)
        popInventory()
        countTransactions(prodID, bankID)
        upAllInv()

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

    queryType = query[0:query.find(" ")]
    if queryType == "SELECT":
        for row in rows:
            data.append((row))

    conn.commit()

    return data

def popInventory():

    """Repopulates the whole inventory filling it with the crossproduct of each product with each location
    """

    #delete any previous rows 
    runSQL("DELETE FROM Inventory;")

    #create crossproduct of prod and bank table
    prods = runSQL("SELECT ID FROM Products")
    banks = runSQL("SELECT ID FROM Locations")
    numLoops = 0
    for i in banks:
        for j in prods:
            runSQL("INSERT INTO Inventory VALUES ("+str(numLoops)+","+str(i[0])+", "+str(j[0])+", 0);")
            #sets each quantity to 0 and each row to 
            numLoops+=1

def countTransactions(prodID, bankID):
    """
    Searches through Transactions in finalProject.mdb adding up donations and subtracting all
    transactions to track an accurate inventory for the specified product at the specified location
    Args:
        prodID: the id of desired product to look for transactions
        bankID: the id of desired location to look for transactions

    Returns:
        count: the stock of the desired inventory
    """
    #Get the count of transactions and donations of the current item at the specified bank
    countDon = runSQL("SELECT Sum(T.Quantity) AS [Sum], T.Trans_Type, T.ProdID, T.LocID FROM Transaction AS T WHERE (((T.ProdID)="+str(prodID)+") AND (T.LocID)="+str(bankID)+") AND T.Trans_Type = 'Donation' GROUP BY T.Trans_Type, T.ProdID, T.LocID;")
    countTrans = runSQL("SELECT Sum(T.Quantity) AS [Sum], T.Trans_Type, T.ProdID, T.LocID FROM Transaction AS T WHERE (((T.ProdID)="+str(prodID)+") AND (T.LocID)="+str(bankID)+") AND T.Trans_Type = 'Transaction' GROUP BY T.Trans_Type, T.ProdID, T.LocID;")
    
    #check whether these exists, else default to 0
    try:
        countDon = countDon[0][0]
    except: #see if there exists any donation history
        countDon = 0

    try:
        countTrans = countTrans[0][0]
    except: #see if there exists any transaction history
        countTrans = 0
    #calc net inventory with donations increasing quantity and transactions depleting it
    count = 0
    count += countDon
    count -= countTrans
    return count

def upAllInv():
    """
    Runs through all the Transaction history to update the inventory quantity for all inventories
    """
    prods = runSQL("SELECT ID FROM Products")
    banks = runSQL("SELECT ID FROM Locations")
    #iterate through all combos of prods and locations
    for i in banks:
        for j in prods:
            #get the net inventory of transactions
            numQuant = str(countTransactions(j[0],i[0]))
            #use this to update the current inventory
            runSQL("UPDATE Inventory SET Quantity ="+numQuant+" WHERE ProdId = "+str(j[0])+" AND BankID = "+str(i[0])+";")

def popTrans():
    prods = runSQL("SELECT ID FROM Products")
    banks = runSQL("SELECT ID FROM Locations")
    lastID = runSQL("SELECT MAX(ID) FROM Transaction")[0][0]
    #iterate through all combos of prods and locations
    prodCyc = 1
    bankCyc = 1
    for i in range (100):
        lastID += 1
        print(str(lastID) +" "+ str(bankCyc)+" " + str(prodCyc))
        if (lastID%3>2):
            runSQL("INSERT INTO Transaction VALUES ("+str(lastID)+", 5, "+str(prodCyc)+", "+str(bankCyc)+", "+str(lastID)+", =Date(), 'Transaction')")
        else:
            runSQL("INSERT INTO Transaction VALUES ("+str(lastID)+", 7, "+str(prodCyc)+", "+str(bankCyc)+", "+str(lastID)+", =Date(), 'Donation')")
        bankCyc += 1
        prodCyc += 1
        if prodCyc > 20:
            prodCyc = 1
            
        if bankCyc > 3: 
            bankCyc = 1

        
    
        
    

