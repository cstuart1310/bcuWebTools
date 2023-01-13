import re

text="""
<div class="clear">
<h4>Similar Courses</h4>
<ul class="no-bullets mln mbn pbn">
<li></li>
<li><a class="simple" href="/fashion-and-textiles/courses/textile-design-ba-hons-with-foundation-2020-21"><span class="mid-grey icon-right-open-mini inline-block pan mvn mll mrs" aria-hidden="true">Textile Design with a Foundation Year - BA (Hons)</a></li>
</ul>
</div>

"""

matches = re.findall(r'">([^<]+)</a>', text)

if matches:
    for match in matches:
        print(match)