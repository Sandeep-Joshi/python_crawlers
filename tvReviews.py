import re
import socket
from selenium import webdriver
import sys


def amazonCrawler(prod, totalReviews, fileWriter):
    websiteUrl = 'http://www.amazon.com'
    count = 0
    driver = webdriver.Chrome( './chromedriver' )
    tab = webdriver.Chrome( './chromedriver' )
    driver.get(websiteUrl)
    # find the search box and search for the product
    driver.find_element_by_id('twotabsearchtextbox').send_keys(prod)
    driver.find_element_by_css_selector('#nav-search > form > div.nav-right > div > input').click()
    while 1:
        # Find the urls for reviews
        prodUrls = re.finditer('.*href=\"(.*customerReviews)">(.*?)<', driver.page_source)
        # (\d+) is not working as , is used for numbers
        for url in prodUrls:  # loops work on different prods on a search page per page
            print url.group(2), url.group(1)
        #   Go to the URL and parse the reviews
            try:
                tab.get(url.group(1))
            except socket.error:
                # sometime error comes from Amazon specially while processing <10000 reviews. Just move on for next prod
                print "Socket error. Moving on to next product page"
                continue
            # get to next page which we get while browsing but not through selenium
            prodUrl = re.search('<a class="a-link-emphasis.*href="(.*)"', tab.page_source).group(1)
            # for reviewUrl in reviewUrls:
            pageUrl = None
            i = 2
            while True:
                try:
                    tab.get(prodUrl)
                    reviews = None
                    reviews = re.finditer(
                        'a-star-(.) review-rating.*(d?).*review-date">on (.*?)</span>.*review-text">(.*?)</span>',
                        tab.page_source)
                except socket.error:
                    # probably last page moving on to new product
                    print 'Last page probably. Moving to next prod'
                    break

                flag = False
                for r in reviews:  # Reviews in a single page for a prod
                    flag = True
                    count += 1
                    try:
                        fileWriter.write(websiteUrl + '\t' + r.group(4).encode('utf-8', 'ignore').strip() + '\t' + r.group(1) + '\t' + r.group(3) + '\n')
                        print r.group(2), r.group(3), r.group(4).encode('utf-8', 'ignore').strip()

                    except UnicodeDecodeError:
                        fileWriter.write(websiteUrl + '\t' + r.group(4).encode('ascii', 'ignore').strip() + '\t' + r.group(1) + '\t' + r.group(3) + '\n')
                        print r.group(2), r.group(3), r.group(4).encode('ascii', 'ignore').strip()
                    finally:
                        if count >= totalReviews:
                            driver.close()
                            tab.close()
                            fileWriter.close()
                            return
                if not flag:
                    # the last page has been reached..go to new product
                    print "nothing found on page"
                    break

                if count >= totalReviews:
                    driver.close()
                    tab.close()
                    fileWriter.close()
                    return
                else:
                    # go to next page for same product by checking its URL
                    #tab.find_element_by_css_selector('#pagnNextLink').click()
                    # Selenium not working so using URLs
                    if not pageUrl:
                        try:
                            pageUrl = re.search('href="(.*pageNumber=2?)"', tab.page_source).group(1).replace(
                                'pageNumber=2', 'pageNumber={}')
                        except AttributeError:
                            # There's no page 2
                            break
                    if pageUrl:
                        # Change the pagenumber
                        prodUrl = pageUrl.format(str(i))
                        print prodUrl
                        i += 1
        # go to next search page in Amazon search
        print "Going to next page"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # driver.find_element_by_css_selector('#pagnNextLink').click()
        driver.find_element_by_class_name("pagnRA").click()


def main(argv):
    fileWriter = open('reviews.txt', 'w')
    amazonCrawler("TV", 30000, fileWriter)

if __name__ == "__main__":
    main(sys.argv)