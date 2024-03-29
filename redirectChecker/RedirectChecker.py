from urllib import request
from urllib import error
from bs4 import BeautifulSoup

import csv
import os

root=os.path.dirname(os.path.abspath(__file__))+"\\"
outFile=open(root+"Redirects.csv","w",newline='')#output spreadsheet
writer = csv.writer(outFile)#starts the writer
header=["Course","URL","Redirects to another page?","Redirect URL","Notes"]#headers to be written to a spreadsheet


writer.writerow(header)#Writes the headers

inpFile=open(root+"links.txt","r")#input list of urls to test
links=inpFile.readlines()
redirects=[]

counter=1#used to display progress
for url in links:
    url=url.replace("\n","")#side effect of reading from txt
    print(counter,"/",len(links)," ",url)
    counter+=1
    try:
        response = request.urlopen(url)#loads page
        code=response.status#status code
        new_url = str(response.geturl())#gets new url
        soup = BeautifulSoup(request.urlopen(url),features="html.parser")#reads the html as soup
        title= (soup.title.string)#gets the page title from soup
    except Exception as e:#Either caused by the url having no destination or network issues
        print("404")
        data=[title,url,"Yes",e]
        writer.writerow(data)#writes the result of this one url to the csv


    if url!=new_url:#if the original url isn't the same as the destination one
        ("Redirect")
        print(url)
        print(new_url)
        redirects.append(url)
        data=[title,url,"Yes",new_url,]
        writer.writerow(data)#writes the result of this one url to the csv
    print("-"*20)



print("Redirects:")
print(len(redirects))

for url in redirects:
    print(url)