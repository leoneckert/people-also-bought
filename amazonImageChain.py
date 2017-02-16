from selenium import webdriver
import time, os, sys, random, urllib
#  import random
#  import ConfigParser
#  from bs4 import BeautifulSoup
#  import urllib
#  from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0

driver = None
output_dir = None

def type_word(input_elem, word):
    for letter in word:
        input_elem.send_keys(letter)
        #  time.sleep(0.1)

def open_amazon():
    global driver
    driver = webdriver.Firefox()
    url = "https://amazon.com"
    driver.get(url)

def make_output_dir(word):
    global output_dir
    ts = int(time.time())
    output_dir = str(ts) + "_" + word
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

def navigate_to_first_item(word):
    global driver
    search_element = driver.find_element_by_css_selector("#twotabsearchtextbox")
    type_word(search_element, word)   
    search_button = driver.find_element_by_css_selector("div.nav-search-submit input.nav-input")
    search_button.click()
    time.sleep(2)
    results = driver.find_elements_by_css_selector("a.s-access-detail-page")
    random_result = random.choice(results)
    random_result.click()

def get_main_image(count):
    global driver
    global output_dir
    #  image = None
    #  image = driver.find_element_by_css_selector("img#landingImage")
    #  url = image.get_attribute("src")
    #  urllib.urlretrieve(url, output_dir + "/" + "{:06d}".format(count) + ".jpg")
    try:
        image = driver.find_element_by_css_selector("img#landingImage")
        url = image.get_attribute("src")
        urllib.urlretrieve(url, output_dir + "/" + "{:06d}".format(count) + ".jpg")
    except:
        print "landingImage didnt work"
        try:
            image = driver.find_element_by_css_selector("img#landingimage")
            url = image.get_attribute("src")
            urllib.urlretrieve(url, output_dir + "/" + "{:06d}".format(count) + ".jpg")
        except:
            print "landingimage didnt work"
            try:
                image = driver.find_element_by_css_selector("img#imgBlkFront")
                url = image.get_attribute("src")
                urllib.urlretrieve(url, output_dir + "/" + "{:06d}".format(count) + ".jpg")
            except:
                print "imgBlkFront didnt work"

def open_next_item():
    global driver
    the_link = None
    headlines = driver.find_elements_by_css_selector("h2.a-carousel-heading")
    for headline in headlines:
        if headline.text == "Customers Who Bought This Item Also Bought":
        #  if headline.text == "Sponsored Products Related To This Item":
            parent = headline.find_element_by_xpath('./..')
            items = parent.find_elements_by_css_selector("li.a-carousel-card")
            while len(items) == 0:
                parent = parent.find_element_by_xpath('./..')
                items = parent.find_elements_by_css_selector("li.a-carousel-card")
                print "in while loop"
            random_item = random.choice(items)
            the_link = random_item.find_element_by_css_selector("a.a-link-normal")
            break
    print the_link
    driver.get(the_link.get_attribute("href"))

if __name__ == "__main__":
    open_amazon()
    time.sleep(2)
    query = sys.argv[1]
    make_output_dir(query)
    navigate_to_first_item(query)
    time.sleep(5)
    get_main_image(0)
    time.sleep(2)
    count = 1
    while True:
        open_next_item()
        time.sleep(2)
        get_main_image(count)
        time.sleep(2)
        count += 1
        #  if count > 10:
        #      break




