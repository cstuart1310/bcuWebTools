import urllib.request #Used to grab the html
from urllib import request

import io #Used to mess with files with weird encoding
import time #Delays
import re
import csv
from bs4 import BeautifulSoup
import os

outFile=open("C:\\Users\\S20103502\\Documents\\GitHub\\bcuWebTools\\USPFinder\\output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 
writer = csv.writer(outFile)#starts the writer

headers=["Title","School","URL","Notes","No of USPs currently on page CALLUM REMOVE CODE WHEN DONE","No of USPs (Auto updates from cells)","USP 1","USP 2","USP 3","USP 4","USP 5","USP 6","USP 7","USP 8","USP 9","USP 10","USP 11","USP 12","USP 13","USP 14","USP 15","Changed by BP? (Y/N)","Change Details"]
writer.writerow(headers)#Writes the headers at the top of the spreadsheet

foundCount=0
foundLinks=[]
errorLinks=[]

def scrape(siteURL):
    #Gets html
    try:
        with urllib.request.urlopen(siteURL) as url: #"Opens" URL (Gets data)
            site = url.read() #Reads the html code
            site=site.decode("utf-8")#Decodes the site
            with io.open(r"C:\\Users\\S20103502\\Documents\\GitHub\\bcuWebTools\\USPFinder\\site.txt", "w", encoding="utf-8") as file:#Writes the site to a file
                file.write(site)
                return True
    except (urllib.error.HTTPError, ValueError):#Error handling for invalid links
        print("Page does not exist!",siteURL)
        errorLinks.append([siteURL,"404'd"])#Adds to array to tell user broken links at end of program
        writer.writerow(["None","",siteURL,"""Page is not public"""])
        return False

def find(siteURL):#Returns a list of USPs for each site
    title=getTitle(siteURL)
    USPList=[title,"",siteURL,"","",""]#Starts the list to have the url and two empty spots for the counters
    replacables=["</li>","<li>","</span>","<span>","</p>","<p>","</strong>","<strong>","""<p class="Default">""","""<span lang="EN-US">""","""<span lang="EN">""","""<span class="normaltextrun">"""]#List of stuff to be removed
    with open(r"C:\\Users\\S20103502\\Documents\\GitHub\\bcuWebTools\\USPFinder\\site.txt", "r", encoding="utf-8") as file:#Reads the file
        
        text=file.read()
        
        #Cuts out the why choose us list section
        try:
            result = text.split("Why Choose Us?")[1]
            result = result.split("</ul>")[0]
            
            lineCount=0#Counter used because repeating html means cant use index to search
            for line in result.split("\n"):#Checks every line
                
                if "<li>" in line:#If the line is a list item
                    USPLine=line#Reassigns the variable so i dont get confused
                    if (USPLine.replace("<li>",""))=="":#If the line is empty without the <li>
                        USPLine=result.split("\n")[lineCount+1]#move to the next line which hopefully has the data
                        USPList[3]="Had to move to next line"
                    for replacable in replacables:#Removes all items from the list (HTML tags)
                        USPLine=USPLine.replace(replacable,"")
                    USPList.append(USPLine)#Adds the line to a list of USPs for this page
                lineCount+=1
            writer.writerow(USPList)#Writes the USPs and the URL to a csv
        except IndexError:
            errorLinks.append([siteURL,"No Why choose us"])
            writer.writerow([title,"",siteURL,"""No "Why Choose us" section found"""])
    



def getTitle(url):
    response = request.urlopen(url)#loads page
    soup = BeautifulSoup(request.urlopen(url),features="html.parser")#reads the html as soup
    title= (soup.title.string)#gets the page title from soup
    return title

#Main

linkFile=open(r"C:\\Users\\S20103502\\Documents\\GitHub\\bcuWebTools\\USPFinder\\links.txt","r")#Opens link file
links = [link.rstrip() for link in linkFile]#Gets links from file without trailing \n
linkFile.close()#Closes the link file for memory conservation
linksLength=len(links)#Stored as a variable for convenience
print("Found",linksLength,"links to look through")
print("This might take a while, begin? y/n (CTRL + C to quit)")
continueInp=input(">")

if continueInp=="y":
    print("---------------")
    siteIndex=0
    for siteURL in links:#Iterates through each URL in the file
        siteIndex+=1#Counter of no of sites checked
        if "https://" not in siteURL:#If it's a poorly thought out seperator so i can do it all at once
            writer.writerow(siteURL)#Writes the USPs and the URL to a csv
        else:
            if scrape(siteURL):#Gets HTML as plain text
                print("Read HTML for site",siteURL,siteIndex,"/",linksLength)
                find(siteURL)#Looks for phrase in HTML

    print("-----Done scraping!-----")

    
    if len(errorLinks)>0:#If there is at least one link that didn't load
        print("-----Links that errored for some reason-----")
        for link in errorLinks:
            print(link[0],link[1])

    os.startfile("C:\\Users\\S20103502\\Documents\\GitHub\\bcuWebTools\\USPFinder\\output.csv")#Opens the output file automatically because I'm lazy

#Quit
elif continueInp=="n":
    print("Quitting")

else:
    print("Invalid input")
