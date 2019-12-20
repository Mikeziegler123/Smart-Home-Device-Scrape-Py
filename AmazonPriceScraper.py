# Author: Michael Ziegler    |     AmazonPriceScraper.py
#
# Program: This program is written to scrape Amazon's website
# using each item's unique 'data-asin identifier' to recreate
# a shortened working url to each item which can be iterated
# through by simply swapping out the data-asin value at the
# end of each url. The program then extracts the data values
# from each item's page, then writes each value to a row in a
# .csv file named 'scraped_data.csv' under the appropriate
# column header.

from lxml import html
import csv
import os
import requests
import builtins
from time import sleep
from builtins import ValueError
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from time import sleep
from random import randint

def parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    try:
        # Retrying for failed requests
        for i in range(20):
            # Generating random sleep delays
            sleep(randint(1,10))
            # Adding verify=False to avold ssl related issues
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200: 
                doc = html.fromstring(response.content)
                XPATH_NAME = '//h1[@id="productTitle"]//text()'
                XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
                XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
                XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
                XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

                RAW_NAME = doc.xpath(XPATH_NAME)
                RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
                RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
                RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
                RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

                NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
                
                SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
                
                CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
                
                ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
                
                AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

                if not ORIGINAL_PRICE:
                    ORIGINAL_PRICE = SALE_PRICE
                    
                # retrying in case of captcha
                if not NAME:
                    raise ValueError('captcha')

                data = {
                    'NAME': NAME,
                    'SALE_PRICE': SALE_PRICE,
                    'CATEGORY': CATEGORY,
                    'ORIGINAL_PRICE': ORIGINAL_PRICE,
                    'AVAILABILITY': AVAILABILITY,
                    'URL': url,
                }
                return data
            # Not found
            elif response.status_code==404:
                break

    except Exception as e:
        print(e)

# ReadAsin(Main Scrape Function): The Asin is a unique product identifier that
# Amazon uses for each of the products it displays. This data is hardcoded in
# for testing purposes, but when complete, will be scraped using a separate
# function which passes the ASIN value to ReadAsin
#
# A visual example(ScreenShot) of the ASIN(s) within the page source code is
# available at the link below:
# https://bit.ly/2sQoiV9
def ReadAsin():
    
    AsinList = ['B07Z6ZV54B',
                'B079QHML21',
                'B075H7Z5L8',
                'B078K432TK',
                'B01EZV35QU',
                'B07DLSNNDS',
                'B0178IC734',
                'B076VRH9WP',
                'B07FVST9YN',
                'B07GGWNQT7',
                'B07HZLHPKP',
                'B07GSTJ8TV',
                'B071LLWLLP',
                'B079MFTYMV',
                'B07G3ZNK4Y',
                'B012ZPKNFE',
                'B0131RG6VK',
                'B07BFRHZLB',
                'B0798KPH5X',
                'B0798DVZCY',
                'B0798GJVTR',
                'B074K427TZ',
                'B07S59MHJ9' ]
    extracted_data = []
    
    # Iterate through each asin in the list, concatenating url stem with asin
    # number to access each item's individual url 
    for i in AsinList:
        url = "http://www.amazon.com/dp/" + i
        print("Processing: " + url)
        
        # Calling the parser
        parsed_data = parse(url)
        if parsed_data:
            extracted_data.append(parsed_data)

    # Writing scraped data to csv file (scraped_data.csv)
    with open('scraped_data.csv', 'w') as csvfile:
        fieldnames = ['NAME','SALE_PRICE','CATEGORY','ORIGINAL_PRICE','AVAILABILITY','URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()    
        for data in extracted_data:
            writer.writerow(data)
#
if __name__ == "__main__":
    ReadAsin()
