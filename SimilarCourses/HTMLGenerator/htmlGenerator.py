import time #Used for timing the program to get estimates
import datetime#used to tell when finished (For when you leave a terminal open for ages and cant remember if you hit run)
import urllib.request #Used to grab the html
from urllib import request
import io #Used to mess with files with weird encoding
import time #Delays
import re
import csv#Used to write the info into a csv
from bs4 import BeautifulSoup #Used just to parse the title of the page
import os
from PIL import Image
from urllib import request



print("\n"*5)
root=os.path.dirname(os.path.abspath(__file__))+"\\"
print("Root Dir:",root)

similarCounter=0
foundCount=0
foundLinks=[]
errorLinks=[]

imgMaxX=2000
imgMaxY=1000

imgMinX=500
imgMinY=100

idLines=open((root+"mediaIds.txt"),"r",encoding="utf-8").readlines()#opens the massive file with ALL the bcu images

try:
    outFile=open(root+"output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 
except PermissionError:
    print("Error: Close the open file")
    time.sleep(10)
    outFile=open(root+"output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 


writer = csv.writer(outFile)#starts the writer
headers=["Title","URL","Faculty","School","Notes","Code"]
writer.writerow(headers)#Writes the headers at the top of the spreadsheet

def initScrape(siteURL):
    global siteIndex
    siteIndex+=1#Counter of no of sites checked
    if "https://" not in siteURL:#If url file contains something that isnt a url
        print(siteURL)
    else:
        if isRedirect(siteURL)==False:#if the page is not a redirect
            site=scrape(siteURL)#Gets HTML as plain text
            printLine=("Read HTML for site:"+siteURL)
            print(printLine+(" "*(150-(len(printLine))))+str(siteIndex)+"/"+str(linksLength)+" "+str(round(((100/linksLength)*siteIndex),2))+"%")#prints lined up %
            
            try:
                writer.writerow([getTitle(site),siteURL,getFaculty(site),getSchool(site),"",compileHTML(siteURL,site)])#writes info from each func into csv
            except AttributeError:
                print("Error:",siteURL)
                writer.writerow(["Error",siteURL,"Error","Error","Error","Error"])
        else:
            writer.writerow(["Redirect",siteURL,"Redirect","Redirect","Redirect","Redirect"])
def isRedirect(url):#checks if the page redirects somewhere else, in which case ignores
    response = request.urlopen(url)#loads page
    new_url = str(response.geturl())#gets new url
    if url==new_url:#If the given URL and the opened URL are the same
        return False#is not a redirect
    else:#If they are different (Redirected)
        print("Page is a redirect")
        return True#is a redirect


def scrape(siteURL):#Gets the source code of the page and writes it into a text file
    global similarCounter
    #Gets html
    try:
        with urllib.request.urlopen(siteURL) as url: #"Opens" URL (Gets data)
            site = url.read() #Reads the html code
            site=site.decode("utf-8")#Decodes the site
            return site
    except (urllib.error.HTTPError, ValueError):#Error handling for invalid links
        print("Page does not exist!",siteURL)
        errorLinks.append([siteURL,"404'd"])#Adds to array to tell user broken links at end of program
        writer.writerow(["None",siteURL,"","","""Page is not public"""])#Writes the error into the csv
        return False
    
def getImageTag(site):
    foundLine=False
    imgTag="""<img src="$IMGURL" alt="$IMGALT" data-source="$IMGDATA">"""#template to be replaced
    imageURL="$MANUALIMAGE"#different replacable so a custom template image can be put in
    imgAlt="Image Alt"
    imgData="1234-567"
    for line in site.split("\n"):#Each line of html from the page
        if "<img" in line and "course__image" in line:#if the course hero is found
            line=line.split(">")[0]#splits so line is just the img line of code
            imageURL=re.findall(r'src="([^"]+)"',line)[0]
            

            #cleanup so we're left with just the url
            imageURLReplacables=['<img src="','" alt','"']
            imageURL=imageURL.replace("&amp;"," ")
            imageURL=imageURL.replace(" ", "%20")

            for replacable in imageURLReplacables:
                imageURL=imageURL.replace(replacable,"")
            print("Image URL:",imageURL)

            
            if checkImageSize(imageURL)==True:#If the image is a good size
                for idLine in idLines:#Reads through each line of the big file
                    if imageURL in idLine:#If a line is found containing the url we're looking for
                        foundLine=True
                        imgAlt=re.findall("""<img\s+.*?alt="(.*?)".*?>""",idLine)[0]#regex filter's the alt text from the line
                        imgData=re.findall("""<img\s+.*?data-source="([^"]*)".*?>""",idLine)[0]#regex filters the data-source from the line
                if foundLine==False:#if the img tag cant be found in the big doc, uses temp data
                    print("Couldn't find image in document, using temp data")
                    imgAlt="Image Alt"
                    imgData="1234-567"

            else:#If image isn't correct resolution
                imageURL="$MANUALIMAGE"#different replacable so a custom template image can be put in
                imgAlt="Image Alt"
                imgData="1234-567"

                #replaces the imgTag template with actual data
    imgTag=imgTag.replace("$IMGURL",imageURL)
    imgTag=imgTag.replace("$IMGALT",imgAlt)
    imgTag=imgTag.replace("$IMGDATA",imgData)

    return imgTag



def checkImageSize(imageURL):
    
    #Downloads URL
    imagePath=root+"sizeCheck.jpg"
    try:
        urllib.request.urlretrieve(imageURL, imagePath)
        im = Image.open(imagePath)
        print("Hero Image Size:",im.size)
        if im.size[0]>=imgMinX and im.size[0]<imgMaxX:
            if im.size[1]>=imgMinY and im.size[1]<=imgMaxY:
                return True
        else:            
            return False
    except Exception as e:
        print(e)

def compileHTML(courseURL,site):
    template='''
    
<div class="similar-courses__card">
    <div class="similar-courses__image">$IMAGETAG</div>
    <div class="similar-courses__text">
    <h4 class="similar-courses__title">$COURSETITLE<span class="similar-course-card__intake">$COURSEENTRY</span></h4>
    <a href="$COURSEURL" class="similar-courses__link"></a></div>
    </div>    
    
    
'''

    replaceImageTag=getImageTag(site)
    replaceCourseTitle=getTitle(site)
    replaceCourseEntry=getEntry(site)
    replaceCourseURL=getURL(courseURL)
    print("Title:",replaceCourseTitle)
    print("Entry Year:",replaceCourseEntry)
    print("URL:",replaceCourseURL)
    print("Image Tag:",replaceImageTag)
    try:
        code=template.replace("$IMAGETAG",getImageTag(site))#getImageTag(site))
    except Exception as e:
        print("Bad img",e)
        #return "Bad img"

    try:
        code=code.replace("$COURSETITLE",getTitle(site))
    except Exception as e:
        print("Bad title",e)
        return "Bad title"
    try:
        code=code.replace("$COURSEENTRY",getEntry(site))
    except:
        print("Bad entry")
        return "Bad entry"
    try:
        code=code.replace("$COURSEURL",getURL(courseURL))
    except:
        print("BadURL")
        return "Bad url"
        #print(code)
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

def getTitle(site):#Gets the title from the url
    for line in site.split("\n"):
        if "<h1>" in line:
            line=line.replace("<h1>","")
            line=line.replace("</h1>","")
            line=re.sub(r"\s{2,}","",line)
            return line

def getEntry(site):#Entry year
    # soup = BeautifulSoup(request.urlopen(url),features="html.parser")#reads the html as soup
    # title= (soup.title.string)#gets the page title from soup
    
    try:
        entry=str(re.findall("202[0-9]/(?:2[0-9]|30) Entry",site)[0])#Looks between 2 and entry in the page (Will need to futureproof since won't work for courses in the year 3000+)
        entry=entry.replace("- ","")
        entry=entry.replace(" -","")
        entry=entry.replace(" |","")
        return entry

    except:
        return False
    

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
    start = time.time()#starts the timer
    siteIndex=0#Index 0 for the pos of the site url in the list
    for siteURL in links:#Iterates through each URL in the file
        print("-"*10)
        initScrape(siteURL)

    print("-----Done scraping!-----")
    end = time.time()#Ends the timer
    timeTaken = end - start#Gets the time it took to scrape and process everything
    print("Finished at",datetime.time)
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