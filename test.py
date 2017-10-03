#! /usr/bin/python

crs = open("db1.txt", "r")
for columns in ( raw.strip().split() for raw in crs ):  
    print(columns[0] +" "+ columns[1])
crs.close
