#! /usr/bin/python

import glob 

# Function definition is here

"Reads data from the txt file"
def readFile(fileName):
    dict = {}
    print("Transactions:")
    crs = open(fileName, "r")
    for columns in ( raw.strip().split() for raw in crs ): 
        dict[columns[0]] = columns[1]
        print(str(columns[0]) + " : "+ str(columns[1]))
    crs.close

    itemsets = list()  
    txnSetList = list() 
    for i in dict.values():
        itemsets = []
        for item in i.split(','):
            itemsets.append(item)
        txnSetList.append(set(itemsets))

    return txnSetList

"Reading the dictionary(database) create a list of unique itemsets and itemsets"
def createUniqueItemSet(database):
    uniqueItems = list()
    itemsets = list()
    for i in database:
        for itemset in i:
            for item in itemset.split(','):
                itemsets.append(item)
                if [item] not in uniqueItems:
                    uniqueItems.append([item])
    #print("uniqueItems: "+str(list(map(frozenset,uniqueItems))))
    #print("itemsets: "+str(itemsets))
    return list(map(frozenset,uniqueItems)), itemsets

"Return the dictionary with itemSet and support"
def scanDB(txnSetList, uniqueItems, min_support):
    key_support={}
    support=0
    for item in uniqueItems:
        support=0
        for txn in txnSetList:
            if item.issubset(txn):
                support= support + 1
            key_support[item]=support

    #print(key_support)
    itemSet = []

    for k, v in list(key_support.items()):
        if v/len(txnSetList)*100 >= min_support:
            itemSet.append(k)
    #print("Itemset: "+str(itemSet))
    #print("Support Data: "+str(key_support))
    return itemSet, key_support

"Returns the new pair of itemsets"
def generateItemsets(itemSet, length):
    subItemSet = list()
    retList = list()
    for x in itemSet:            
        subItemSet = set([x.union(y) for x in itemSet for y in itemSet if len(x.union(y)) == length])    
    
    for i in subItemSet:
         retList.append(i)
    #print("New pair of itemsets: "+str(retList))
    return retList

def generateAssociationRules(L, key_support, min_confidence):
    rules = []
    for i in range(1, len(L)):
        for Item in L[i]:
            rhs = [frozenset([item]) for item in Item]
            #print("Item"+ str(Item)+ ' rhs '+str(rhs))
            if (i > 1):
                generateMoreRules(Item, rhs, key_support, rules, min_confidence)
            else:
                findConfidence(Item, rhs, key_support, rules, min_confidence)
    return rules

def getConfidence(key_support, freqItemSet, postSet):
    return (key_support[freqItemSet] / key_support[freqItemSet - postSet]) * 100


"Returns the rule that satisfies minimum confidence criteria"
def findConfidence(freqItemSet, rhs, key_support, rules, min_confidence):
    ruleWithMinConf = []
    for postSet in rhs:
        #confidence = (key_support[freqItemSet] / key_support[freqItemSet - postSet]) * 100
        confidence = getConfidence(key_support, freqItemSet,postSet)
        if (confidence >= min_confidence):
            preSet = freqItemSet-postSet
            print(preSet,'-->',postSet,'confidence:',confidence)
            rules.append((preSet, postSet, confidence))
            ruleWithMinConf.append(postSet)
    return ruleWithMinConf

"This function generates more rules from our data"
def generateMoreRules(Item, rhs, key_support, rules, min_confidence):    
    l2 = len(Item)
    l1 = len(rhs[0])    
    if (l2 > (l1 + 1)):
        newRhs = generateItemsets(rhs, l1 + 1)
        newRhs = findConfidence(Item, newRhs,  key_support, rules, min_confidence)
        if (len(newRhs) >= 0):
            generateMoreRules(Item, newRhs, key_support, rules, min_confidence)


#################################
min_support = 20
min_confidence = 50
files = glob.glob('*.txt')
for file in files:
    print("****************************************")
    print(file)
    txnSetList = readFile(file)   #reading (database) file as list of list of transactions

    #print("List of transactions: "+str(txnSetList))

    uniqueItems, itemsets = createUniqueItemSet(txnSetList)

    itemSet1, key_support = scanDB(txnSetList, uniqueItems, min_support)
    print(itemSet1)
    itemSet = [itemSet1] 
    #print("Initial itemset: "+str(itemSet))
    k = 2   #size of itemsets to create 
    while(len(itemSet[k-2]) >= 1):
    #while(candidateKeys != set([])):
        print("test: "+str(itemSet[k - 2]))
        candidateKeys = generateItemsets(itemSet[k - 2], k)
        newItemSets, k_s = scanDB(txnSetList, candidateKeys, min_support)
        key_support.update(k_s)
        itemSet.append(newItemSets)
        k += 1

    #print("Final:" +str(itemSet))
    #print("Key with Support:" +str(key_support))
    print("Association Rules:")
    rules = generateAssociationRules(itemSet, key_support, min_confidence)
    #print("rules: "+str(rules))
    print("****************************************")