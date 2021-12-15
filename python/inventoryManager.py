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

        getTransactions(userID)
        
        
        
"""

import runSQL

def countTransactions(prodID, bankID):
    #Get the count of transactions of the current item at the specified bank
count = runSQL.runSQL("SELECT Sum(T.Quantity) AS [Sum], T.Trans_Type, T.ProdID, T.LocID FROM Transaction AS T, Inventory AS I WHERE (((T.ProdID)="+prodID+") AND ((T.LocID)=" +bankID+ "))GROUP BY T.Trans_Type, T.ProdID, T.LocID;")
print (count)
try:
    count = count[0][0]
except: #see if there exists a 
    return False
print ("returning:" +str(count))
return count

def getInventory(prodID, bankID):
    currInv = runSQL.runSQL("SELECT I.Quantity"+
        "\nFROM Inventory as I"+
        "\nWhere I.prodID = "+prodID+" and I.bankID = "+bankID+";")
print ("returning:" +str(currInv))
return currInv


def modInventory(prodID, bankID):
    #check if row exists with this number
    inv = getInventory(prodID, bankID)
    
    runSQL.runSQL("UPDATE Inventory SET Quantity="+str(countTransactions(prodID,bankID)[0][0]) WHERE ProdID="+prodID+" and BankID = "+bankID+";")
    

def createInventory():
    runSQL.popInventory()

def getTransactions(userID):
    runSQL.runSQL("SELECT L.Name, P.Name,T.Quantity,T.Trans_Type, T.Trans_Date FROM Transaction as T, Products as P, Locations as L WHERE T.ProdID = P.ID and T.LocID = L.ID and T.UserID ="+str(userID)+";")
