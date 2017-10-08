#! /usr/bin/python

from itertools import chain, combinations

# Function definition is here

# reads data from the txt file 
def readFile(fileName):
    dict = {}
    crs = open(fileName, "r")
    for columns in ( raw.strip().split() for raw in crs ): 
        dict[columns[0]] = columns[1]
    crs.close

    itemsets = list()  
    txnSetList = list() 
    for i in dict.values():
        itemsets = []
        for item in i.split(','):
            itemsets.append(item)
        txnSetList.append(set(itemsets))

    return txnSetList

# Reading the dictionary(database) create a list of unique itemsets and itemsets
def createUniqueItemSet(database):
    uniqueItems = list()
    itemsets = list()
    for i in database:
        for itemset in i:
            for item in itemset.split(','):
                itemsets.append(item)
                if [item] not in uniqueItems:
                    uniqueItems.append([item])
    print("uniqueItems: "+str(list(map(frozenset,uniqueItems))))
    #print("itemsets: "+str(itemsets))
    return list(map(frozenset,uniqueItems)), itemsets

# Return the dictionary with itemSet and support 
def scanDB(txnSetList, uniqueItems, min_support):
    dict={}
    support=0
    for item in uniqueItems:
        support=0
        for txn in txnSetList:
            if item.issubset(txn):
                support= support + 1
            dict[item]=support

    print(dict)
    itemSet = []

    for k, v in list(dict.items()):
        if v/len(txnSetList)*100 >= min_support:
            itemSet.append(k)
    dict = {}
    print("Itemset: "+str(itemSet))
    return itemSet

#Returns the new pair of itemsets
def generateItemsets(Lk, k): 
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
    print("New pair of itemsets: "+str(retList))
    return retList


#################################
min_support = 50
min_confidence = 70
txnSetList = readFile("db1.txt")    #reading (database) file as list of list of transactions
print("List of transactions: "+str(txnSetList))

uniqueItems, itemsets = createUniqueItemSet(txnSetList)

itemSet1 = scanDB(txnSetList, uniqueItems, min_support)

itemSet = [itemSet1] 
print("Initial itemset: "+str(itemSet))
k = 2
while(len(itemSet[k-2]) > 0):
#while(itemSet == []):
    candidateKeys = generateItemsets(itemSet[k - 2], k)
    newItemSets = scanDB(txnSetList, candidateKeys, min_support)
    #support_data.update(supK)
    itemSet.append(newItemSets)
    k += 1

print("Final:" +str(itemSet))




    










