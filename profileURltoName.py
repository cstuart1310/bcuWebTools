file=open("URLs.txt","r")

prefix=input("Prefix before name:")

for url in file.readlines():
    url=url.replace(prefix,"")
    url=url.replace("-"," ")
    url=url.replace("\n","")
    url = url.title()
    print(url)