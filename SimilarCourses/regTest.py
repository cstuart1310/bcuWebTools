import re

text="""
<h4>Similar Courses</h4>
<ul class="no-bullets mln mbn pbn">
<li><a class="simple" href="/courses/music-industries-ba-hons-2019-20"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true">Music Industries - BA (Hons)</a></li>
<li><a class="simple" href="/conservatoire/courses/music-technology-bsc-honours-2019-20
"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true">Music Technology - BSc (Hons)</a></li>
<li><a class="simple" href="/conservatoire/courses/bmus-honours-jazz-2019-20"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true">Jazz - BMus (Hons)</a></li>
</ul>
</div>
"""

# matches = re.findall(r'">([^<]+)</a>', text)
# USPList=[]
# USPList.append(matches)
# for match in matches:
#     print(match)

USPList=[]
result = text.split("Similar Courses")[1]
result = result.split("</ul>")[0]
#result=re.sub("[0-9]\n","",result)
lineCount=0#Counter used because repeating html means cant use index to search
for line in result.split("\n"):
    print(line)
    #copy paste
    if "<li>" in line:#If the line is a list item
        USPLine=line#Reassigns the variable so i dont get confused
        if (USPLine.replace("<li>",""))=="":#If the line is empty without the <li>
            USPLine=result.split("\n")[lineCount+1]#move to the next line which hopefully has the data
        USPLine=USPLine.replace("</span>","")#Removes spans so that course names can consistently be regexed out even with inconsistent code
        USPLine=re.findall(r'">([^<]+)</a>',USPLine)#Finds the course name (Filters for a-z after ">  )
        USPList.append(USPLine)#Adds the line to a list of USPs for this page

print(USPList)