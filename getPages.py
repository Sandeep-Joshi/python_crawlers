"""
This script reads the file that was created by getFreelancerUsers.py line-by-line.
Each line contains the url to the profile page of a freelancer. The script then downloads
the profile page for each url and stores it in a new file. The name of the new file should
be the same as the username of the corresponding freelancer.

 """ 
 
# import the libraries we will be using
import urllib2
import os
import re
from collections import Counter

# make a new browser
browser = urllib2.build_opener()
browser.addheaders = [('User-agent', 'Mozilla/5.0')]

rank_limit = 150


# if the folder doesn't exist, make it 
# if not os.path.exists(outFolder):  # use path.exists() from the os library to check if something exists
#     os.mkdir(outFolder)  # use mkdir() from the os library to make a new directory
path = os.path.dirname(os.path.abspath(__file__))

# open a connection to the file you want to read
# fileReader = open(path + '\input.txt')
fileReader = open('input.txt')
# fileWriter = open(path + '\\top_skill_counts.txt', 'w')
fileWriter = open('top_skill_counts.txt', 'w')

# Regex to find the values
# reg = "(\d+).*" +item  # this regex was to get the
reg = '"profile-skill-amount">(\d+)'
top_skill = []

for line in fileReader:  # this syntax allows us to read the file line-by-line
    link = line.strip()  # .strip() removes white spaves and line-change characters
    # from the beginning and end of a string

    # build url
    url = "https://www.freelancer.com/u/{}.html".format(link)
    print 'Donwloading: ', url

    # use the browser to get the link and read the html into a variable
    html = browser.open(url).readlines()

    for htmlLine in html:
        values = re.finditer(reg, htmlLine)
        for val in values:
            if int(val.group(1)) >= rank_limit and temp:
                tags = re.finditer(">(.*)</a>", temp)
                for tag in tags:
                    top_skill.append(tag.group(1))
            elif (val.group(1)) < rank_limit:
                break  # These were sorted in descending order in page. no need to go on
        temp = htmlLine

# count all the skills in the list
count = Counter()
for skill in top_skill:
    count[skill] += 1

# Save this list in the file
for tech, count in count.most_common():
    fileWriter.write(tech + ':' + str(count) + "\n")

fileWriter.close()
fileReader.close()
