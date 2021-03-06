"""Everything about running SQL commands is stored here

    Currently, this only has runSQL on /assets/finalProject.mdb
    Methods:
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
        runSQL(query)
=======
>>>>>>> Stashed changes
        def runSQL(query):
        
        def popInventory()
        def upAllInv()
        def getProdInv(ProdId)
        def clearInv()
        def incrementQuant(prodID, bankID, step)
        def decrementQuant(prodID, bankID, step)
        
<<<<<<< Updated upstream
        def countTransactions(prodID, bankID)
=======
        def countTrans(prodID, bankID)
>>>>>>> Stashed changes
        def getAllTrans(userID)
        def popTrans(numPop)
        def clearTransPast(invID)
        def clearTrans()
        
        def addTransaction(userID, prodID, bankID, quantity)
        def addDonation(userID, prodID, bankID, quantity)
        
    
        
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes

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
    clearInv()

    #create crossproduct of prod and bank table
    prods = runSQL("SELECT ID FROM Products")
    banks = runSQL("SELECT ID FROM Locations")
    numLoops = 0
    for i in banks:
        for j in prods:
#<<<<<<< Updated upstream
            invCount = countTransactions(j[0],i[0])
            runSQL("INSERT INTO Inventory VALUES ("+str(numLoops)+","+str(i[0])+", "+str(j[0])+", "+str(invCount)+");")
            #sets each quantity to 0 and each row to 
            numLoops+=1

#=======
#<<<<<<< Updated upstream
            runSQL("INSERT INTO Inventory VALUES ("+str(numLoops)+","+str(i[0])+", "+str(j[0])+", 0);")
            #sets each quantity to 0 and each row to 
            numLoops+=1

#=======
            invCount = countTrans(j[0],i[0])
            runSQL("INSERT INTO Inventory VALUES ("+str(numLoops)+","+str(i[0])+", "+str(j[0])+", "+str(invCount)+");")
            #sets each quantity to 0 and each row to 
            numLoops+=1

#>>>>>>> Stashed changes
def upAllInv():
    """
    Brute Force Runs through all the Transaction history to update the inventory quantity for all inventories
    """
    prods = runSQL("SELECT ID FROM Products")
    banks = runSQL("SELECT ID FROM Locations")
    #iterate through all combos of prods and locations
    for i in banks:
        for j in prods:
            #get the net inventory of transactions
#<<<<<<< Updated upstream
            numQuant = str(countTransactions(j[0],i[0]))
#=======
            numQuant = str(countTrans(j[0],i[0]))
#>>>>>>> Stashed changes
            #use this to update the current inventory
            runSQL("UPDATE Inventory SET Quantity ="+numQuant+" WHERE ProdId = "+str(j[0])+" AND BankID = "+str(i[0])+";")


def getProdInv(ProdId):
    """
    Args:
    ProdId: the id of the product to search the inventories for
    Returns:
    query: holds all the quantities and names of each bank for the specified product
    """

    #"Get the Inventory of [Product] at multiple locations"
    query = runSQL("SELECT I.Quantity, L.Name, FROM Inventory as I, Locations as L WHERE L.ID = I.BankID AND I.ProdID ="+str(ProdId)+";")
    return query


def clearInv():
    #"Turn the Inventory into a Blank Slate"
    runSQL("DELETE FROM Inventory")


def incrementQuant(prodID, bankID, step):
    try:
#<<<<<<< Updated upstream
        print("in inc")
        numCurrInv = countTrans(prodID, bankID) + step
#=======
        print("in inc- step: "+str(step))
        numCurrInv = countTrans(prodID, bankID)
        print("got "+str(numCurrInv))
        numCurrInv += step
#>>>>>>> Stashed changes
        print("changing quant to "+str(numCurrInv))
        #"Donate [step] number of [product] to [bank]" -> "Increase the inventory of [product] at [bank] by [step]"
        runSQL("UPDATE Inventory SET Quantity ="+str(numCurrInv)+" WHERE ProdId = "+str(prodID)+" AND BankID = "+str(bankID)+";")
    except:
        return False


def decrementQuant(prodID, bankID, step):
    try:
#<<<<<<< Updated upstream
        print("in dec")
        numCurrInv = countTrans(prodID, bankID) - step
#=======
        print("in dec- step: "+str(step))
        numCurrInv = countTrans(prodID, bankID)
        print("got "+str(numCurrInv))
        numCurrInv -= step
#>>>>>>> Stashed changes
        print("changing quant to "+str(numCurrInv))
        #"Remove [step] number of [product] from [bank]" -> "Decrease the inventory of [product] at [bank] by [step]"
        runSQL("UPDATE Inventory SET Quantity ="+str(numCurrInv)+" WHERE ProdId = "+str(prodID)+" AND BankID = "+str(bankID)+";")
    except:
        return False

def countTrans(prodID, bankID):
#>>>>>>> Stashed changes
    """
    Searches through Transactions in finalProject.mdb adding up donations and subtracting all
    transactions to track an accurate inventory for the specified product at the specified location
    Args:
        prodID: the id of desired product to look for transactions
        bankID: the id of desired location to look for transactions

    Returns:
        count: the stock of the desired inventory
    """
#<<<<<<< Updated upstream
#=======
    print("1")
#>>>>>>> Stashed changes
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
#<<<<<<< Updated upstream
    count = 0
    count += countDon
    count -= countTrans
#=======
    print("2")
    count = 0
    count += countDon
    count -= countTrans
    print("returning " + str(count))
#>>>>>>> Stashed changes
    return count


def getAllTrans(userID):
    """
    retreives the transaction information for every transaction made by the specified user
    The Product name, the name of the food bank, the quantity exchanged and whether it was a donation or a transaction
    
    Args: userID: the user requesting to se their transaction history
    """
    try:
        queryRet = runSQL("SELECT P.Name, L.Name, T.Quantity, T.Trans_Type FROM Transaction as T, Products as P, Locations as L WHERE T.ProdID = P.ID AND T.LocID = L.ID AND T.UserID = "+str(userID)+";")
        return queryRet
    except:
        return False


def popTrans(numPop):
    """
    Adds numPop many rows to the Transaction Table
    Args:numPop - the desired number of new rows to make
    """
   
    #create bounds to keep the User iterator in
        #assumes there are no gaps in UserIDs
    lowUserID = runSQL("SELECT MIN(UserID) FROM Users")[0][0]
    highUserID = runSQL("SELECT MAX(UserID) FROM Users")[0][0]
    currUserID = lowUserID

    prodCyc = (numPop%40) +1
    bankCyc = (numPop%3) + 1

    #Create numPop 
    for i in range (numPop):
        #print(str(currUserID)+" "+ str(bankCyc)+" " + str(prodCyc))
        #for pseudorandomness, every 3rd Transaction is a Transaction (not a Donation)
        if (i%3>1):
            addTransaction(str(currUserID), (prodCyc), str(bankCyc), str(i%bankCyc+prodCyc))
        else:
            addDonation(str(currUserID), (prodCyc), str(bankCyc), str(i%prodCyc+bankCyc))

        #increment other values
        bankCyc += 1
        prodCyc += 1
        currUserID += 1
        #adjust for out of bounds errors
        if prodCyc > 40:
            prodCyc = 1
        if bankCyc > 3: 
            bankCyc = 1
        if currUserID > highUserID:
            currUserID = lowUserID

            
def clearTransPast(invID):
    #"Remove all transactions after ID [invID]"
    runSQL("DELETE FROM Transaction as T WHERE T.ID > "+str(invID))

def clearTrans():
    #"Blank Slate for the Transaction table"
    runSQL("DELETE FROM Transaction")

def addTransaction(userID, prodID, bankID, quantity):
    #"Get the ID of the last transaction"
    lastID = runSQL("SELECT MAX(ID) FROM Transaction")[0][0]
    #check in case there are no indexes
    if lastID == None:
        lastID = 0
    try:
        #"Create a record for this transaction
        runSQL("INSERT INTO Transaction VALUES ("+str(lastID+1)+", "+str(userID)+", "+str(prodID)+", "+str(bankID)+", "+str(quantity)+", =Date(), 'Transaction')")
        #"Remove [quantity] number of [product] from [bank]"
        decrementQuant(prodID, bankID, quantity)
    except:
        return False


def addDonation(userID, prodID, bankID, quantity):
    lastID = runSQL("SELECT MAX(ID) FROM Transaction")[0][0]
    if lastID == None:
        lastID = 0
    
    try:
        #"Create a record for this donation"
        runSQL("INSERT INTO Transaction VALUES ("+str(lastID+1)+", "+str(userID)+", "+str(prodID)+", "+str(bankID)+", "+str(quantity)+", =Date(), 'Donation')")
        #"Donate [quantity] number of [product] to [bank]"
        incrementQuant(prodID, bankID, quantity)
    except:
         return False

"""
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes

"""
