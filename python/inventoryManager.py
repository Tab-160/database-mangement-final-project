""" deals with inventory management

    Methods:
        countTransactions()
        modInventory()
        getInventory()
        createInventory()
            DELETE FROM Inventory;
            create crossproduct of prod and bank table
                INSERT INTO Inventory
                VALUES (id, bank, prod, 0);
        
        
        
"""

import runSQL

def countTransactions(prodID, bankID):
    #Get the count of transactions of the current item at the specified bank
count = runSQL.runSQL("SELECT Sum(T.Quantity) AS [Sum], T.Trans_Type, T.ProdID, T.LocID" +
    +"\nFROM Transaction AS T, Inventory AS I\n"
    +"\nWHERE (((T.ProdID)="+prodID+") AND ((T.LocID)=" +bankID+ "))\n"
    +"\nGROUP BY T.Trans_Type, T.ProdID, T.LocID;")

try:
    count = count[0][0]
except: #see if there exists a 
    return False

def getInventory(prodID, bankID):
    currInv = runSQL.runSQL("SELECT I.Quantity"+
        "\nFROM Inventory as I"+
        "\nWhere I.prodID = "+prodID+" and I.bankID = "+bankID+";")


return count

def modInventory(prodID, bankID):
    #check if row exists with this number
    getInventory
    
    runSQL.runSQL("UPDATE Inventory"+
    "SET Quantity="+countTransactions(prodID,bankID)+""+
    "\nWHERE ProdID="+prodID+" and BankID = "+bankID+";")
    
    return true

def createInventory():
            #delete any previous rows 
            runSQL.runSQL("DELETE FROM Inventory;")

            #create crossproduct of prod and bank table
            numProds = runSQL.runSQL("SELECT COUNT(P.ID)"
                +"\nFROM Products as P")
            numBanks = = runSQL.runSQL("SELECT COUNT(L.ID)"
                +"\nFROM Locations as L")
            numLoops = 0
            for (i in range(numBanks))
                for (j in range (numProds))
                    runSQL.runSQL("INSERT INTO Inventory"+
                        "\nVALUES ("+numLoops+","+i+", "+j+", 0);")
                    #sets each quantity to 0 and each row to 
                    numLoops++