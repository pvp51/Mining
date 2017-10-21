#! /usr/bin/python
t = frozenset()
t = frozenset({'a'})
print(t)
z = set()
z = t
print(set(t))

# def joinSet(itemSet, length):
#     subItemSet = list()
#     retList = list()
#     for i in itemSet:            
#         subItemSet = set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])    
    
#     for i in subItemSet:
#          retList.append(i)
#     print(retList)
#     return retList

# itemSet = [frozenset({'B'}), frozenset({'C'}), frozenset({'D'}), frozenset({'A'})]
# name = joinSet(itemSet, 2)
# print(name)

# while (len(newRhs) >= 2):
#             l1 = len(newRhs[0])    
#             if (l2 > (l1 + 1)):
#                 newRhs = generateItemsets(newRhs, l1 + 1)
#                 newRhs = findConfidence(Item, newRhs,  key_support, rules, min_confidence)
#             else:
#                 break

#             if (len(newRhs) > 1):
#             generateMoreRules(Item, newRhs, key_support, rules, min_confidence)


# def generateItemsets(Lk, k): 
#     retList = []
#     lenLk = len(Lk)
#     for i in range(lenLk):
#         for j in range(i+1, lenLk): 
#             L1 = list(Lk[i])[:k-2]
#             L2 = list(Lk[j])[:k-2]
#             L1.sort()
#             L2.sort()
#             if L1==L2: #if first k-2 elements are equal
#                 retList.append(Lk[i] | Lk[j]) #set union
#     print("New pair of itemsets: "+str(retList))
#     return retList