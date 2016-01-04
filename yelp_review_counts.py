__author__ = 'joshi'

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
# path = os.path.dirname(os.path.abspath(__file__))

# open a connection to the file you want to read
# fileReader = open(path + '\input.txt')
fileReader = open('input.txt')
fileWriter = open('output.txt', 'w')

# Regex to find the values
# reg = "(\d+).*" +item  # this regex was to get the
# reg = '("author".*"review review..with-sidebar?")'
# prof regex: "/freelancer/skills/.*"<(.*)</a>"  # to find the skill
reviews = {};


def get_int(str):
    try:
        return int(str)
    except ValueError:
        return 0


def count_votes(regex, str):
    sum = 0
    vals = re.finditer(regex, str)
    # print(regex, str)
    for val in vals:
        sum += get_int(val.group(1))
    return sum


for line in fileReader:  # this syntax allows us to read the file line-by-line
    link = line.strip()  # .strip() removes white spaves and line-change characters
    # from the beginning and end of a string

    # use the browser to get the link and read the html into a variable
    html = browser.open(link).readlines()
    html_cache = ''
    author_cache = ''
    author = ''
    a = ''
    sum_votes = 0
    for htmlLine in html:
        # Get the author
        try:
            author = re.search('"author" content="(.*?)"', htmlLine).group(1)
        except AttributeError:
            # do nothing
            html = html

        if len(author) <= 0:
            continue

        # append rest of lines (not clear why yet)
        reg_use = re.compile(r'"useful".*?"count">(\d*)<?.*?</li>', re.DOTALL)
        reg_cool = re.compile(r'"cool".*?"count">(\d*)<?.*?</li>', re.DOTALL)
        reg_funny = re.compile(r'"funny".*?"count">(\d*)<?.*?</li>', re.DOTALL)
        if(len(html_cache) > 0) and author != author_cache:
            # if author_cache=='Nicole O.':
            #     print html_cache.strip()
            # print author, author_cache
            # This is second time we are getting it so save the string so far and work on it
            # extract other values from this block
            try:
                votes = 0
                # votes = get_int(re.search(reg_use, html_cache).group(1))
                votes = count_votes(reg_use, html_cache)
                sum_votes += votes
                # print 'useful' + str(votes)
            except:
                # do nothing
                a = a

            try:
                votes = 0
                # votes = get_int(re.search(reg_funny, html_cache).group(1))
                votes = count_votes(reg_funny, html_cache)
                # print 'funny' + str(votes)
                sum_votes += votes
            except AttributeError:
                # do nothing
                a =a
            try:
                votes = 0
                # votes = get_int(re.search(reg_cool, html_cache).group(1))
                votes = count_votes(reg_cool, html_cache)
                # print 'cool' + str(votes)
                sum_votes += votes
            except:
                # do nothing
                a = a

            # print author_cache + str(sum_votes)
            if len(author_cache) > 0:
                if reviews.get(author_cache):
                    reviews[author_cache] = int(reviews.get(author_cache)) + sum_votes
                else:
                    reviews[author_cache] = sum_votes
            sum_votes = 0
            # clear the cache
            html_cache = ''
            author_cache = author

        html_cache += htmlLine
    # At last append the last user
    # print author_cache + str(sum_votes)
    if len(author_cache) > 0:
        if reviews.get(author_cache):
            reviews[author_cache] = int(reviews.get(author_cache)) + sum_votes
        else:
            reviews[author_cache] = sum_votes

for user in sorted(reviews.keys()):
    fileWriter.write(user + '\t' + str(reviews[user]) + '\n')
    # print user, '\t', reviews[user]



# # Save this list in the file
# for tech, count in count.most_common():
#     fileWriter.write(tech + ':' + str(count) + "\n")

fileWriter.close()
fileReader.close()
