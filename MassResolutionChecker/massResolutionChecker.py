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


print("\n"*5)
root=os.path.dirname(os.path.abspath(__file__))+"\\"
print("Root Dir:",root)

similarCounter=0
foundCount=0
foundLinks=[]
errorLinks=[]

imgMaxX=1200
imgMaxY=450

imgMinX=1200
imgMinY=450
imgLeeway=1.1#%

try:
    outFile=open(root+"output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 
    outFileSingleCourse=open(root+"outputSingleCourse.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 
except PermissionError:
    print("Error: Close the open file")
    time.sleep(10)
    outFile=open(root+"output.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 
    outFileSingleCourse=open(root+"outputSingleCourse.csv","w",newline='', encoding="utf-8-sig")#output spreadsheet Excel requires the UTF-8-encoded BOM code point 

singleCourseWriter = csv.writer(outFileSingleCourse)#starts the writer for course name, image 1, image 2, image 3
writer = csv.writer(outFile)#starts the writer
headers=["Title","Page URL","Size X","Size Y","File Size (KB)","Type","Image URL","Status"]
writer.writerow(headers)#Writes the headers at the top of the spreadsheet

def initScrape(siteURL):
    global siteIndex
    siteIndex+=1#Counter of no of sites checked
    if "https://" not in siteURL:#If url file contains something that isnt a url
        print(siteURL)
    else:
        if isRedirect(siteURL)==False:#If the page is not a redirect (Is still online)
            site=scrape(siteURL)#Gets HTML as plain text
            printLine=("Read HTML for site:"+siteURL)
            print(printLine+(" "*(150-(len(printLine))))+str(siteIndex)+"/"+str(linksLength)+" "+str(round(((100/linksLength)*siteIndex),2))+"%")#prints lined up %
            imageURLs,headerType=getImageURL(site)
            print("Header Type:",headerType)
            print("Checking",len(imageURLs),"URLs")
            imageSizes=[getTitle(site),siteURL]
            for imageURL in imageURLs:
                imageURL="".join(imageURL)#the worst way to fix this
                sizeX,sizeY,fileSize = checkImageRes(imageURL)
                
                writer.writerow([getTitle(site),siteURL,sizeX,sizeY,fileSize,headerType,imageURL,sizeChecks(sizeX,sizeY,headerType)])#writes info from each func into csv
                imageSizes.append([sizeX,sizeY])
            singleCourseWriter.writerow(imageSizes)#writes info from each func into csv

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
    
def sizeChecks(sizeX,sizeY,headerType):
    if headerType=="Hero":
        idealSizeX,idealSizeY=1200,450
        
    elif headerType=="Gallery":
        idealSizeX,idealSizeY=1600,900
    
    leewaySizeXMax=int(idealSizeX*imgLeeway)
    leewaySizeYMax=int(idealSizeY*imgLeeway)
    leewaySizeXMin=int(idealSizeX//imgLeeway)
    leewaySizeYMin=int(idealSizeY//imgLeeway)

    print("Ideal Size",idealSizeX,idealSizeY)
    print("Leeway Size Upper",leewaySizeXMax,leewaySizeYMax)
    print("Leeway Size Lower",leewaySizeXMin,leewaySizeYMin)

    if sizeX==idealSizeX and sizeY==idealSizeY:
        print("Ideal Size")
        return "Ideal"
    elif sizeX>=leewaySizeXMin and sizeX<=leewaySizeXMax and sizeY>=leewaySizeYMin and sizeY<=leewaySizeYMax:
        print("Ideal with leeway")
        return "Ideal with leeway"
    else:
        print("Needs to be changed")
        return "Needs to be changed"
    
def getImageURL(site):
    foundLine=False
    imageURLs=None
    headerType="None"
    #gets the url if its' a hero image
    for line in site.split("\n"):#Each line of html from the page
        if "<img" in line and "course__image" in line:#if the course hero is found
            line=line.split(">")[0]#splits so line is just the img line of code
            imageURLs=re.findall(r'src="([^"]+)"',line)
            headerType="Hero"
            print("Image URLs:",imageURLs)
            return imageURLs, headerType    
            #stops looking through the file
        elif "swiper swiperCourseGallery" in line:#if this is found meaning the course has a gallery
            galleryImageSection=site.split("swiper swiperCourseGallery")[1]#after this bit
            galleryImageSection=galleryImageSection.split("swiper-button-prev")[0]#before this bit
            imageURLs=re.findall(r'src="([^"]+)',galleryImageSection)#finds the src="www.rrjrrjewrjoiejorijo" bit
            headerType="Gallery"
            #stops looking through the file
            print("Image URLs:",imageURLs)
            return imageURLs, headerType    


def getResolution(imagePath):
    im = Image.open(imagePath)
    return im.size

def checkImageRes(imageURL):
    
    #Downloads URL
    imagePath=root+"sizeCheck.jpg"
    imageURL=imageURL.replace(" ", "%20")
    try:
        urllib.request.urlretrieve(imageURL, imagePath)
    except:
        print("Error, waiting and retrying")
        time.sleep(10)
        urllib.request.urlretrieve(imageURL, imagePath)
    im = Image.open(imagePath)
    fileSize=str(int(os.path.getsize(imagePath))/1000)
    print("Image Size:",im.size)
    return im.size[0],im.size[1],fileSize


def getTitle(site):#Gets the title from the url
    for line in site.split("\n"):
        if "<h1>" in line:
            line=line.replace("<h1>","")
            line=line.replace("</h1>","")
            line=re.sub(r"\s{2,}","",line)
            return line

def isRedirect(url):#checks if the page redirects somewhere else, in which case ignores
    response = request.urlopen(url)#loads page
    new_url = str(response.geturl())#gets new url
    if url==new_url:#If the given URL and the opened URL are the same
        return False#is not a redirect
    else:#If they are different (Redirected)
        print("Page is a redirect")
        return True#is a redirect

def getURL(url):#Gets the url in a domain-less format
    url=url.replace("https://www.bcu.ac.uk","")
    return url
#Main

linkFile=open(root+"links.txt","r")#Opens link file
links = [link.rstrip() for link in linkFile]#Gets links from file without trailing \n
linkFile.close()#Closes the link file for memory conservation
linksLength=len(links)#Stored as a variable for convenience
print("Found",linksLength,"links to look through")


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