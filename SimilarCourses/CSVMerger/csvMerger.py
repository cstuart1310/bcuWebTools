import os
import csv


print("\n"*5)
root=os.path.dirname(os.path.abspath(__file__))+"\\"
print("Root Dir:",root)


#opens the csv of courses with their similar children, and the csv containing each individual similar code
codeCSV=csv.reader(open(root+"code.csv","r",newline='', encoding="utf-8-sig"), delimiter=' ', quotechar='|')#output spreadsheet Excel requires the UTF-8-encoded BOM code point
coursesCSV=csv.reader(open(root+"courses.csv","r",newline='', encoding="utf-8-sig"), delimiter=' ', quotechar='|')#output spreadsheet Excel requires the UTF-8-encoded BOM code point


#sets up output file
outCSV=open(root+"output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 
writer = csv.writer(outCSV)#starts the writer
headers=["Title","URL","Faculty","School","Combined Codes"]
writer.writerow(headers)#Writes the headers at the top of the spreadsheet


for courseRow in coursesCSV:
    print(courseRow)