# -*- coding: utf-8 -*-
import re

def printA1c(value, row, line, regexlevel):

    #Check if the passed value is float or not
    try:
        float(value)
    except ValueError:
        # String just write it
        newfile.write(value + '\t' + regexlevel + '\t' + line + "\n")
        return

    print value
    if value.find("%") > -1:
        if float(value[:-1]) < 26:
            # newfile.write("in Row " + str(row) + " a1c level is " + value + "\n")
            newfile.write(value + '\t' + regexlevel + '\t' + line + "\n")
        else:
            # newfile.write("in Row " + str(row) + " a1c level cannot be predicted " + "\n")
            newfile.write('-' + '\t' + regexlevel + '\t' + line + "\n")
    else:
        if float(value) < 26:
            # newfile.write("in Row " + str(row) + " a1c level is " + value + "\n")
            newfile.write(value + '\t' + regexlevel + '\t' + line + "\n")
        else:
            # newfile.write("in Row " + str(row) + " a1c level cannot be predicted " + "\n")
            newfile.write('-' + '\t' + regexlevel + '\t' + line + "\n")

file_conn=open('data.txt')
row = 1
newfile=open('a1cresults.xls','w')

for line in file_conn:
    line=line.strip()
    index = line.find("a1c")
    index = 1
    if index > -1:
        # newline = line[index+3:]
        newline = line[0:] + " "
        newline = newline.replace("&#39;","'")
        # To help identify number i.e 3, -> 3 ,
        newline = newline.replace(", ", " ")
        # Add a gap to each numeral
        # fixing crawl issue should be ...
        newline = re.sub('&hellip;', ' ... ', newline)
        # fixing crawl issue should be &
        newline = re.sub('&amp;|&', 'and', newline)
        # adds a space after number i.e. 6% -> 6 % and 6to -> 6 to
        newline = re.sub('(?!a1c)(.)(\d+)([^\.\s\d])', r'\1\2 \3', newline)
        # Adds a space before a number i.e.  6to8 -> 6to 8  please not this would break dates with space might cause issue
        newline = re.sub('(?!a1c)([a-zA-Z;-])([\d+])', r'\1 \2', newline)
        # remove numeric values with different units and numbers greater than 29
        newline = re.sub("(\d+.\d+|\d+).(?=lbs|\$|kg|day|year|lbs|pound|month|mg|liter|hr|minute)|(\d{3,}|[3-9]\d)", "", newline)

        m = re.findall(r'[\s-](\d+\.\d+|\d+)[\s\%\-]', newline)
        print '#', m, newline
        if len(m) == 1:
            printA1c(m[0], row, newline, '1')
        else:
            # more than 1 number found. print words around A1c and around the numbers found

            # check if there's a 'to' between two numbers print later on
            # d = re.findall(r"a1c.*?(of|at|is|to|was)(.*?) (\d+\.\d+|\d+)", newline)
            d = re.findall(r".*?(of|at|is|to|was)(.*?) (\d+\.\d+|\d+)", newline)
            if len(d) > 0:
                skip = False
                for item in d:
                    print '^', item
                    # if more than two matches find the one with a1c ... is  . If there otherwise too hard to tell which a1c
                    # is the right one
                    if item[0] == "is":
                        # print 'item =', item[1], item[2], '|', newline
                        if item[1].__len__() < 35:
                            printA1c(item[2], row, newline, '2')
                            skip = True
                            break
                if (skip == False):
                    for item in d:
                        if len(item) == 3:
                            # print 'item;', item[1], item[2]
                            # print newline
                            # check if line has too many spaces
                            if len(item[1]) < 35:
                                printA1c(item[2], row, newline, '2')
                                break
            else:
                # between 6 and 7 or 6-7 check
                # Maybe also add a1c check here
                d = re.findall(r"((?:between|btw).(?:\d+\.\d+|\d+) ?(?:-|to|and) ?(?:\d+\.\d+|\d+))", newline)
                if len(d) > 0:
                    for item in d:
                        printA1c(d[0], row, newline, '3')
                        break
                else:
                    # See if there's a1c followed quickly by a number and that number only consider it a1c. i.e. inject
                    # some inaccuracies
                    d = re.findall(r"a1c(.*?)(\d+\.\d+|\d+)", newline)
                    if len(d) == 1:
                        for item in d:
                            if len(item[0]) < 17:
                                printA1c(item[1], row, newline, '4')
                            else:
                                printA1c('0.0', row, newline, '0')
                            break
                    else:
                        printA1c('0.0', row, newline, '0')
    else:
         # No prediction
        printA1c('0.0', row, newline, '0')
    row+=1

file_conn.close()
newfile.close()