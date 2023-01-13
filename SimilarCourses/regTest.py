import re

text="""
<h4>Similar Courses</h4>
<p><a class="simple" href="/courses/computer-and-data-science-bsc-hons-2022-23"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true"></span>Computer and Data Science - BSc (Hons)</a></p>
<p><a class="simple" href="/courses/computer-games-technology-bsc-hons-msci-2021-22"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true"></span>Computer Games Technology - BSc (Hons) / MSci</a></p>
<p><a class="simple" href="/courses/visual-effects-bsc-hons-2021-22"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true"></span>Visual Effects - BSc (Hons)</a></p>
<p><a class="simple" href="/courses/digital-media-computing-bsc-hons-2021-22"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true"></span>Digital Media Computing - BSc (Hons</a>)</p>
"""

# matches = re.findall(r'">([^<]+)</a>', text)
# USPList=[]
# USPList.append(matches)
# for match in matches:
#     print(match)

USPList=[]
result = text.split("Similar Courses")[1]
result = result.split("</ul>")[0]
result=re.sub("[0-9]\n","",result)
lineCount=0#Counter used because repeating html means cant use index to search
for line in result.split("\n"):
    print(line)
    #copy paste
    if "<li>" in line:#If the line is a list item
        USPLine=line#Reassigns the variable so i dont get confused
        if (USPLine.replace("<li>",""))=="":#If the line is empty without the <li>
            USPLine=result.split("\n")[lineCount+1]#move to the next line which hopefully has the data
        USPLine=USPLine.replace("-","")#Removes spans so that course names can consistently be regexed out even with inconsistent code
        USPLine=re.findall(r'">([^<]+)</a>',USPLine)#Finds the course name (Filters for a-z after ">  )
        USPList.append(USPLine)#Adds the line to a list of USPs for this page

print(USPList)