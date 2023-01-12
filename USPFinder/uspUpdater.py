import csv

#get updated spreadsheet
prevUSPFile=open("C:\\Users\\S20103502\\Documents\\GitHub\\bcuWebTools\\USPFinder\\prev2.csv",newline='', encoding="utf-8-sig")
currUSPFile=open("C:\\Users\\S20103502\\Documents\\GitHub\\bcuWebTools\\USPFinder\\curr2.csv",newline='', encoding="utf-8-sig")

prevCSVReader = csv.reader(prevUSPFile)
currCSVReader = csv.reader(currUSPFile)

prevRows=[]
currRows=[]

URLMatchCounter=0
URLErrors=[]

def index_2d(myList, v):#Looks through 2d list for value
    for i, x in enumerate(myList):
        if v in x:
            return i, x.index(v)
    return False


#Populate arrays
for prevRow in prevCSVReader:
    prevRows.append(prevRow)

for currRow in currCSVReader:
    currRows.append(currRow)


#Checks URLs
for course in prevRows[1:2]:
    prevUrl=course[1]
    currURLIndex=(index_2d(currRows, prevUrl))
    if currURLIndex==False:
        print(prevUrl,"Not in current!")
        URLErrors.append([prevUrl,"Missing"])
    elif isinstance(currURLIndex[0],int):#If the URL matches (Points to array index)
        URLMatchCounter+=1 #stats
        for USPCount in range(1,15):#Loops through all 15 USP's
            prevUSP=course[7+USPCount]
            print("USP",USPCount,":",prevUSP,"\n")
            currUSP=currRows[currURLIndex[USPCount]]
        

    else:
        URLErrors.append([currURLIndex[0],"Missing"])


print("URL matches:")
print(URLMatchCounter,"/",len(prevRows),"Matched")
print(len(URLErrors),"/",len(prevRows),"not matched")













    # prevUSPs=course[8:16]#Array of all USPs in the current loaded course
    # currUSPs=currRows[currURLIndex[0]]
    #print(prevUSPs)
    # print(currUSPs)
    # print("-"*30)
#    currUSPs=currRows[1][8:16]#Array of all USPs in the current loaded course

# if prevRows[1] == currRows[1]:
#     print("Same")
# else:
#     print("Diff")