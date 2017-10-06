#! /usr/bin/python

# Function definition is here

# reads data from the txt file 
def readFile(fileName):
    dict = {}
    crs = open(fileName, "r")
    for columns in ( raw.strip().split() for raw in crs ):
        dict[columns[0]] = columns[1] 
    crs.close
    return dict

# Reading the dictionary(database) create a list of unique itemsets and itemsets
def createUniqueItemSet(database):
    uniqueItemsets = []
    itemsets=[]
    for itemset in database.values():
        for item in itemset.split(','):
            itemsets.append(item)
        uniqueItemsets = set(itemsets)
    return uniqueItemsets, itemsets

# Return the dictionary with itemSet and support 
def createItemSet(uniqueItemsets, itemsets):
    dict = {}
    support=0
    for item in uniqueItemsets:
        support=0
        if item in itemsets:
            support=itemsets.count(item)
            dict[item] = support
    return dict

# Return the dictionary with itemSet and support 
def updateGlobalDict(globalDict):
    for k, v in list(globalDict.items()):
        if v/len(db)*100 < min_support:
            del globalDict[k]
    return globalDict

def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
    return retList

db = {}
min_support = 50
min_confidence = 70
db = readFile("db1.txt")    #reading (database) file in the dictionary
print(db.values())
uniqueItemsets = set([])
itemsets=[]

uniqueItemsets, itemsets = createUniqueItemSet(db)

print("uniqueItemsets: "+str(uniqueItemsets))
print("itemsets: "+str(itemsets))

itemSet1 = {}
itemSet1 = createItemSet(uniqueItemsets,itemsets) #create C1 as in HW1 sol.

print("ItemSet1: "+str(itemSet1))

globalDict = {} #global dictionary to hold all valid itemsets for association rules
globalDict = itemSet1   

print("GlobalDict: "+str(globalDict))

globalDict = updateGlobalDict(globalDict)

print("GlobalDict after removing itemset below min. support: "+str(globalDict))

returnList = []
keys = []
length = len(globalDict)
for i in globalDict.keys(): #putting keys of dictionary in a list
    keys.append(i)
KeySet = set(keys)  #creating a set out of a list to call aprioriGen method
print("KeySet: "+str(KeySet) + " Length: " + str(length))

returnList = aprioriGen(KeySet,2)
print("Return List: "+str(returnList))


    










