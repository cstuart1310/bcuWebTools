import time #Used for timing the program to get estimates
import urllib.request #Used to grab the html
from urllib import request
import io #Used to mess with files with weird encoding
import time #Delays
import re
import csv#Used to write the info into a csv
from bs4 import BeautifulSoup #Used just to parse the title of the page
import os
from PIL import Image


print("-"*30)
from concurrent.futures import ThreadPoolExecutor, wait
root=os.path.dirname(os.path.abspath(__file__))+"\\"
print("Root Dir:",root)

similarCounter=0
foundCount=0
foundLinks=[]
errorLinks=[]

def initScrape(siteURL):
    global siteIndex
    siteIndex+=1#Counter of no of sites checked
    if "https://" not in siteURL:#If url file contains something that isnt a url
        print(siteURL)
    else:
        site=scrape(siteURL)#Gets HTML as plain text
        printLine=("Read HTML for site:"+siteURL)
        print(printLine+(" "*(150-(len(printLine))))+str(siteIndex)+"/"+str(linksLength)+" "+str(round(((100/linksLength)*siteIndex),2))+"%")
        print(getImageTag(site))
        
        #findUSPs(siteURL,site)#Looks for phrase in HTML

def scrape(siteURL):#Gets the source code of the page and writes it into a text file
    global similarCounter
    #Gets html
    try:
        with urllib.request.urlopen(siteURL) as url: #"Opens" URL (Gets data)
            site = url.read() #Reads the html code
            site=site.decode("utf-8")#Decodes the site
            return site
    except (urllib.error.HTTPError, ValueError):#Error handling for invalid links
        print(e)
        print("Page does not exist!",siteURL)
        errorLinks.append([siteURL,"404'd"])#Adds to array to tell user broken links at end of program
        writer.writerow(["None",siteURL,"","","""Page is not public"""])#Writes the error into the csv
        return False

def getImageTag(site):
    for line in site.split("\n"):
        if "<img" in line and "course__image" in line:
            print("found")
            line=line.split(">")[0]
            checkImageSize(line)
            return line
    return "None found"

def checkImageSize(imageTag):
    #gets the URL from the tag
    imageURL=re.findall(r'src="([^? ]+)',imageTag)[0]
    print("URL",imageURL)
    imageURLReplacables=['<img src="','" alt','"']
    imageURL=imageURL.replace("&amp;"," ")
    for replacable in imageURLReplacables:
        imageURL=imageURL.replace(replacable,"")
    
    #Downloads URL
    print(imageURL)
    imagePath=root+"test.jpg"
    print(imagePath)
    print("Downloading")
    try:
        urllib.request.urlretrieve(imageURL, imagePath)
        print("Downloaded")
        im = Image.open(imagePath)
        print("Size:",im.size)
    except Exception as e:
        print(e)

def compileHTML(courseURL):
    template="""
    
<div class="similar-courses__card">
    <div class="similar-courses__image">$IMAGETAG</div>
    <div class="similar-courses__text">
    <h4 class="similar-courses__title">$COURSETITLE<span class="similar-course-card__intake">$COURSEENTRY</span></h4>
    <a href="$COURSEURL" class="similar-courses__link"></a></div>
    </div>    
    
    
    """

    code=template.replace("$IMAGETAG",getImageTag(courseURL))
    code=code.replace("$COURSETITLE",getTitle(courseURL))
    code=code.replace("$COURSEENTRY",getEntry(courseURL))
    code=code.replace("$COURSEURL",getURL(courseURL))
    print(code)
    return code

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
    soup = BeautifulSoup(request.urlopen(url),features="html.parser")#reads the html as soup
    title= (soup.title.string)#gets the page title from soup
    return title

def getEntry(url):#Entry year
    entry=getTitle(url)
    entry=re.findall("[-].*[-]",entry)[0]
    entry=entry.replace("- ")
    entry=entry.replace(" -")
    return entry

def getURL(url):#Gets the url in a domain-less format
    url=url.replace("https://www.bcu.ac.uk","")
    return url
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
    #Writes the average to the txt for the next run to make an estimate
    averageFile=open(root+"averageTime.txt","w")
    averageFile.write(str(timeTaken/linksLength))
    averageFile.close()

    # try:
    #     os.startfile(root+"output.csv")#Opens the output file automatically because I'm lazy
    # except AttributeError:
    #     print("Error auto-opening spreadsheet.")
#Quit
elif continueInp=="n":
    print("Quitting")

else:
    print("Invalid input")