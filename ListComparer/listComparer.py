import os

#Sees if items in list A are in list B
print("\n"*5,"-"*10)
root=os.path.dirname(os.path.abspath(__file__))+"\\"

listAFile=open(root+"ListA.txt","r")
listBFile=open(root+"ListB.txt","r")
matchesFile=open(root+"matches.txt","w")
dontMatchesFile=open(root+"dontMatches.txt","w")

listA=listAFile.readlines()
listB=listBFile.readlines()

matches=[]
dontMatches=[]

print("List A contains",len(listA),"items")
print("List B contains",len(listB),"items")

print("Checking for matches")
for itemA in listA:
    for itemB in listB:
        if itemB==itemA:
            matches.append(itemA)
            matchesFile.write(str(itemA))




print("Checking for dontMatches...")
for itemA in listA:
    if itemA not in matches:
        dontMatches.append(itemA)
        dontMatchesFile.write(str(itemA))

print("Saving...")
matchesFile.close()
dontMatchesFile.close()
print("Done")

print("-"*10)
print("Matches:",len(matches))
print("Don't matches:",len(dontMatches))