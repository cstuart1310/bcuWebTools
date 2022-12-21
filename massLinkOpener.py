import webbrowser
import time

URLfile=open(r"C:\Users\S20103502\Documents\Work\Tools\massURLs.txt","r")

urls=URLfile.readlines()

for url in urls:
    webbrowser.open(url)
    time.sleep(0.2)