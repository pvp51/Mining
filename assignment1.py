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
    key_support={}
    support=0
    for item in uniqueItems:
        support=0
        for txn in txnSetList:
            if item.issubset(txn):
                support= support + 1
            key_support[item]=support

    print(key_support)
    itemSet = []

    for k, v in list(key_support.items()):
        if v/len(txnSetList)*100 >= min_support:
            itemSet.append(k)
    print("Itemset: "+str(itemSet))
    print("Support Data: "+str(key_support))
    return itemSet, key_support

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

def generateAssociationRules(L, support_data, min_confidence):
    rules = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            print("freqSet"+ str(freqSet)+ ' H1 '+str(H1))
            if (i > 1):
                generateMoreRules(freqSet, H1, support_data, rules, min_confidence)
            else:
                findConfidence(freqSet, H1, support_data, rules, min_confidence)
    return rules


def findConfidence(freqSet, H, support_data, rules, min_confidence):
    "Evaluate the rule generated"
    pruned_H = []
    for conseq in H:
        conf = (support_data[freqSet] / support_data[freqSet - conseq]) * 100
        if conf >= min_confidence:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            rules.append((freqSet - conseq, conseq, conf))
            pruned_H.append(conseq)
    return pruned_H


def generateMoreRules(freqSet, H, support_data, rules, min_confidence):
    "Generate a set of candidate rules"
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = generateItemsets(H, m + 1)
        Hmp1 = findConfidence(freqSet, Hmp1,  support_data, rules, min_confidence)
        if len(Hmp1) > 1:
            generateMoreRules(freqSet, Hmp1, support_data, rules, min_confidence)


#################################
min_support = 20
min_confidence = 50
txnSetList = readFile("db2.txt")    #reading (database) file as list of list of transactions
print("List of transactions: "+str(txnSetList))

uniqueItems, itemsets = createUniqueItemSet(txnSetList)

itemSet1, key_support = scanDB(txnSetList, uniqueItems, min_support)

itemSet = [itemSet1] 
print("Initial itemset: "+str(itemSet))
k = 2   #size of itemsets to create 
while(len(itemSet[k-2]) >= 1):
#while(candidateKeys != set([])):
    candidateKeys = generateItemsets(itemSet[k - 2], k)
    newItemSets, k_s = scanDB(txnSetList, candidateKeys, min_support)
    key_support.update(k_s)
    itemSet.append(newItemSets)
    k += 1

print("Final:" +str(itemSet))
print("Key with Support:" +str(key_support))

rules = generateAssociationRules(itemSet, key_support, min_confidence)
print(rules)


