import time #Used for timing the program to get estimates
import urllib.request #Used to grab the html
from urllib import request
import io #Used to mess with files with weird encoding
import time #Delays
import re
import csv#Used to write the info into a csv
from bs4 import BeautifulSoup #Used just to parse the title of the page
import os

print("-"*30)
from concurrent.futures import ThreadPoolExecutor, wait
root=os.path.dirname(os.path.abspath(__file__))+"//"
print("Root Dir:",root)

try:
    outFile=open(root+"output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 
except PermissionError:
    print("Error: Close the open file")
    time.sleep(10)
    outFile=open(root+"output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 

writer = csv.writer(outFile)#starts the writer
headers=["Title","URL","Faculty","School","Notes","No of similar courses currently on page CALLUM REMOVE CODE WHEN DONE","No of similar courses (Auto updates from cells)","Similar Course 1","Similar Course 2","Similar Course 3","Similar Course 4","Similar Course 5","Similar Course 6","Similar Course 7","Similar Course 8","Similar Course 9","Similar Course 10","Similar Course 11","Similar Course 12","Similar Course 13","Similar Course 14","Similar Course 15","Changed by BP? (Y/N)","Change Details"]
writer.writerow(headers)#Writes the headers at the top of the spreadsheet

similarCounter=0
foundCount=0
foundLinks=[]
errorLinks=[]

possibleReplacable=[]#List to warn user of possible lines that need to be replaced

def scrape(siteURL):#Gets the source code of the page and writes it into a text file
    global similarCounter
    #Gets html
    try:
        with urllib.request.urlopen(siteURL) as url: #"Opens" URL (Gets data)
            site = url.read() #Reads the html code
            site=site.decode("utf-8")#Decodes the site
            if "similar" in site.lower():
                similarCounter=similarCounter+1
            return site
    except (urllib.error.HTTPError, ValueError):#Error handling for invalid links
        print("Page does not exist!",siteURL)
        errorLinks.append([siteURL,"404'd"])#Adds to array to tell user broken links at end of program
        writer.writerow(["None",siteURL,"","","""Page is not public"""])#Writes the error into the csv
        return False

def findsimilars(siteURL,site):#Returns a list of similars for each site
    global similarCounter # Cba to return val
    similarList=[getTitle(siteURL),siteURL,getFaculty(site),getSchool(site),"","",""]#Starts the list to have the url and two empty spots for the counters
    text=site        
    #Cuts out the why choose us list section
    try:
        result = text.split("Similar Courses")[1]
        result = result.split("</ul>")[0]
        result=re.sub("[0-9]\n","",result)#Fixes random line breaks ending in numbers
        lineCount=0#Counter used because repeating html means cant use index to search
        for line in result.split("\n"):#Checks every line
            
            if "<li>" in line or "<p>" in line:#If the line is a list item (Or p tag because these things arent consistent)
                similarLine=line#Reassigns the variable so i dont get confused
                if (similarLine.replace("<li>",""))=="":#If the line is empty without the <li>
                    similarLine=result.split("\n")[lineCount+1]#move to the next line which hopefully has the data
                    similarList[4]="Had to move to next line"
                # for replacable in replacables:#Removes all items from the list (HTML tags)
                #     similarLine=similarLine.replace(replacable,"")
                similarLine=similarLine.replace("</span>","")#Removes spans so that course names can consistently be regexed out even with inconsistent code
                similarLine=re.findall(r'">([^<]+)</a>',similarLine)#Finds the course name (Filters for a-z after ">  )
                # if len(similarLine[0])==0:
                #      similarLine.append("MANUAL CHECK")
                similarList.append(similarLine)#Adds the line to a list of similars for this page
            lineCount+=1
        writer.writerow(similarList)#Writes the similars and the URL to a csv
    except IndexError:
        errorLinks.append([siteURL,"No Why choose us"])
        writer.writerow([getTitle(siteURL),siteURL,getFaculty(site),getSchool(site),"""No similar section found"""])#Writes the error to the csv
    
def getFaculty(site):#Gets the faculty name from the site file
    facultyReplacables=["""                    <span class="value">""","""                    ""","\n"]
        
    text=site
    
    #Cuts out the why choose us list section
    try:
        result = text.split("""<span class="title">Faculty</span>""")[1]
        result = result.split("</span>")[0]
        faculty=result.replace("""<span class="value">""","")
        faculty=result
        for replacable in facultyReplacables:
            faculty=faculty.replace(replacable,"")

    except:
        faculty="Can't find faculty"
    return faculty

def getSchool(site):#Gets the school name from the site file
    schoolReplacables=["""                    <span class="value">""","""                    ""","\n"]
        
    text=site
    
    #Cuts out the why choose us list section
    try:
        result = text.split("""<span class="title">School</span>""")[1]
        result = result.split("</span>")[0]
        school=result
        for replacable in schoolReplacables:
            school=school.replace(replacable,"")
    except:
        school="Can't find school"
    return school

def getTitle(url):#Gets the title from the url
    #response = request.urlopen(url)#loads page
    soup = BeautifulSoup(request.urlopen(url),features="html.parser")#reads the html as soup
    title= (soup.title.string)#gets the page title from soup
    return title

def initScrape(siteURL):
    global siteIndex
    siteIndex+=1#Counter of no of sites checked
    if "https://" not in siteURL:#If url file contains something that isnt a url
        print(siteURL)
    else:
        site=scrape(siteURL)#Gets HTML as plain text
        printLine=("Read HTML for site:"+siteURL)
        print(printLine+(" "*(150-(len(printLine))))+str(siteIndex)+"/"+str(linksLength)+" "+str(round(((100/linksLength)*siteIndex),2))+"%")
        findsimilars(siteURL,site)#Looks for phrase in HTML



#Main

linkFile=open(root+"links.txt","r")#Opens link file
links = [link.rstrip() for link in linkFile]#Gets links from file without trailing \n
linkFile.close()#Closes the link file for memory conservation
linksLength=len(links)#Stored as a variable for convenience
print("Found",linksLength,"links to look through")

replacables=[replacable.rstrip() for replacable in open(root+"replacables.txt","r").readlines()]#Gets links from file without trailing \n
#print("Replacables:",replacables)



averageFile=open(root+"averageTime.txt","r")#opens the file containing the previous average value
averageTime=averageFile.read()#reads the prev average value
if averageTime!="":#If there is data
    print("Task approximate time:",round((float(averageTime)*linksLength),1),"seconds ",end="")#Converts the average time from a str to a float
    if float(averageTime)*linksLength>120:#If the estimated time is more than 2 mins
        print("("+str(round((float(averageTime)*linksLength)/60,1))+" minutes)")#Prints the estimated time converted into minutes
print("\nThis might take a while, begin? y/n (CTRL + C to quit)")
continueInp=input(">")#Doesn't immediately begin due to long processing time needed

if continueInp=="y":#Confirm start
    print("---------------")
    futures=[]
    start = time.time()#starts the timer
    siteIndex=0#Index 0 for the pos of the site url in the list
    with ThreadPoolExecutor() as executor:
        for siteURL in links:#Iterates through each URL in the file
            futures.append(executor.submit(initScrape, siteURL))

    wait(futures)

    print("-----Done scraping!-----")
    end = time.time()#Ends the timer
    timeTaken = end - start#Gets the time it took to scrape and process everything
    
    if len(errorLinks)>0:#If there is at least one link that didn't load
        print("-----Links that errored for some reason-----")
        for link in errorLinks:
            print(link[0],link[1])

    print("-"*30)
    print("Scraped and outputted",linksLength,"courses in",timeTaken,"seconds")#Outputs time taken

    print("\n"*2,"Stats")
    print("Est time:",float(averageTime)*linksLength,"seconds")
    print("Actual time:",timeTaken,"seconds")
    print("Average time per course:",timeTaken/linksLength,"seconds")#Outputs average time per course
    print("\nFound",len(possibleReplacable),"phrases that possibly need replacing:")
    print(possibleReplacable)
    print("Courses with similar courses mentioned:",similarCounter)    
    #Writes the average to the txt for the next run to make an estimate
    averageFile=open(root+"averageTime.txt","w")
    averageFile.write(str(timeTaken/linksLength))
    averageFile.close()

    try:
        os.startfile(root+"output.csv")#Opens the output file automatically because I'm lazy
    except AttributeError:
        print("Error auto-opening spreadsheet.")
#Quit
elif continueInp=="n":
    print("Quitting")

else:
    print("Invalid input")
