import webbrowser
import time
import os
root=os.path.dirname(os.path.abspath(__file__))+"//"

URLfile=open(root+"massURLs.txt","r")

urls=URLfile.readlines()
urlCounter=0
for url in urls:
    urlCounter+=1
    webbrowser.open(url)
    print(url)
    time.sleep(0.5)