__author__ = 'joshi'

# import the libraries we will be using
import urllib2
import time
import re
# import msvcrt
from collections import Counter

# make a new browser
browser = urllib2.build_opener()
browser.addheaders = [('User-agent', 'Mozilla/5.0')]

date_format = "%m/%d/%Y"
cuttoff_date = time.strptime('7/1/2010', date_format)

# if the folder doesn't exist, make it
# if not os.path.exists(outFolder):  # use path.exists() from the os library to check if something exists
#     os.mkdir(outFolder)  # use mkdir() from the os library to make a new directory
# path = os.path.dirname(os.path.abspath(__file__))

# open a connection to the file you want to read
# fileReader = open(path + '\input.txt')
fileReader = open('profile.txt')
fileWriter = open('type_freqs.txt', 'w')

# Regex to find the values
# reg = "(\d+).*" +item  # this regex was to get the
# reg = '("author".*"review review..with-sidebar?")'
# prof regex: "/freelancer/skills/.*"<(.*)</a>"  # to find the skill
tags = {};

reg_checkin = re.compile(r'<i  class=".*?checkin.*?"></i> (\d*) check-in.*?</span>', re.DOTALL)
reg_cat = re.compile(r'<span class="category-str-list">.*?>(.*?)</span>', re.DOTALL)
reg_date = re.compile(r'<span class="rating-qualifier">(.*?)<', re.DOTALL)


def get_int(strn):
    try:
        return int(strn)
    except ValueError:
        return 0


def count_checkins(regex, str, date):
    sum = 0
    vals = re.finditer(regex, str)
    for val in vals:
        sum += get_int(val.group(1))

    # Check the date
    if date > cuttoff_date and sum > 0:
        sum -= 1
    return sum


def extract(htmlString):
    a = 1
    try:
        # Check the date
        date = time.strptime(re.search(reg_date, htmlString).group(1).strip(), date_format)
        print time.strftime('%d/%m/%Y', date)
    except:
        a = a

    try:
        visit = 0
        # c = msvcrt.getch()
        visit = count_checkins(reg_checkin, htmlString, date)
        print visit
    except:
        a = a

    try:
        # find all the categories
        categories = []
        categories = re.findall('>(.*?)</a>', '>' + re.search(reg_cat, htmlString).group(1))
        print categories
    except:
        a = a

    return visit, categories

nextlink = ''


for line in fileReader:  # this syntax allows us to read the file line-by-line
    link = line.strip()  # .strip() removes white spaces and line-change characters
    # from the beginning and end of a string
    pagenumber = 0
    # Loop for each review pages
    while True:
        exit_flag = True
        print link
        # use the browser to get the link and read the html into a variable
        html = browser.open(link).readlines()
        html_cache = ''
        reviewId_cache = ''
        reviewId = ''
        a = ''


        for htmlLine in html:
            # Find the review id to split the html in to chunks whenever new id comes
            try:
                reviewId = re.search('data-review-id="(.*?)" data-signup-object', htmlLine).group(1)
                exit_flag = False
            except AttributeError:
                # do nothing
                html = html

            if len(reviewId) <= 0:
                continue

            # append rest of lines (not clear why yet)
            if(len(html_cache) > 0) and reviewId != reviewId_cache:
                # This is second time we are getting it so save the string so far and work on it
                # extract other values from this block
                visits, taglist = extract(html_cache)

                if len(reviewId_cache) > 0:
                    for tag in taglist:
                        if tags.get(tag):
                            tags[tag] = int(tags.get(tag)) + visits
                        else:
                            tags[tag] = visits

                # clear the cache
                html_cache = ''
                reviewId_cache = reviewId


            html_cache += htmlLine

        # At last append the last user
        # print author_cache + str(sum_votes)
        if len(reviewId_cache) > 0:
            visits, taglist = extract(html_cache)
            for tag in taglist:
                if tags.get(tag):
                    tags[tag] = int(tags.get(tag)) + visits
                else:
                    tags[tag] = visits

        if exit_flag:
            break # exit the loop
        pagenumber += 10
        # Change link to new page
        if len(nextlink) <= 0:
            nextlink = link + '&rec_pagestart={}'

        link = nextlink.format(str(pagenumber))



for user in sorted(tags.keys()):
    if tags[user] > 0:
        fileWriter.write(user + ',' + str(tags[user]) + '\n')
    # print user, '\t', reviews[user]



# # Save this list in the file
# for tech, count in count.most_common():
#     fileWriter.write(tech + ':' + str(count) + "\n")

fileWriter.close()
fileReader.close()
