import webbrowser
import time

URLfile=open("massURLs.txt","r")

urls=URLfile.readlines()

for url in urls:
    webbrowser.open(url)
    time.sleep(0.2)