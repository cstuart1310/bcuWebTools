import csv

#get updated spreadsheet
prevUSPFile=open("prev.csv")
prevCSVReader = csv.reader(prevUSPFile)

currCSVReader = csv.reader(currUSPFile)

prevRows=[]

for prevRow in prevCSVReader:
    prevRows.append(prevRow)


print(prevRows)