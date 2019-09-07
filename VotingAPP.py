from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType
import os
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from os import listdir
from os.path import isfile, join
from selenium.common.exceptions import NoSuchElementException
import random




co = webdriver.ChromeOptions()
co.add_experimental_option("excludeSwitches",
                           ["ignore-certificate-errors", "safebrowsing-disable-download-protection",
                            "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

co.add_argument('--disable-infobars')
co.add_argument('--disable-extensions')
co.add_argument('--profile-directory=Default')
co.add_argument("--incognito")
co.add_argument("--disable-plugins-discovery")
co.add_argument("--start-maximized")

def get_proxies(co=co):
    with open("proxy.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    PROXIES = [x.strip() for x in content]

    return PROXIES


def proxy_driver(PROXIES, co=co):

    prox = Proxy()

    if PROXIES:
        pxy = PROXIES[-1]
    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()


    proxy = Proxy()
    proxy.proxyType = ProxyType.MANUAL
    proxy.autodetect = False
    proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = pxy
    co.Proxy = proxy
    co.add_argument("ignore-certificate-errors")
    driver = webdriver.Chrome(executable_path="D:/chromedriver.exe",chrome_options=co)

    return driver



def firstsite(driver):
    item_url = "https://www.research.net/r/ClimateControlExperts"
    driver.get(item_url)
    delay = 5
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'checkbox-button-container')))
        print("Page is ready!")

        checkboxs = driver.find_elements_by_css_selector("span.checkbox-button-label-text.question-body-font-theme.user-generated")

        for check in checkboxs:
            driver.execute_script("arguments[0].click();", check)
            time.sleep(1)
        submit = driver.find_element_by_tag_name("button")
        driver.execute_script("arguments[0].click();", submit)
        time.sleep(1)

    except TimeoutException:
        print("Page Loading took too much time!")



def secondsite(driver):
    item_url = "https://www.research.net/r/NationalTechnicalInstitute"
    driver.get(item_url)
    delay = 5
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'checkbox-button-container')))
        print("Page is ready!")

        checkboxs = driver.find_elements_by_css_selector("span.checkbox-button-label-text.question-body-font-theme.user-generated")

        for check in checkboxs:
            driver.execute_script("arguments[0].click();", check)
            time.sleep(1)
        submit = driver.find_element_by_tag_name("button")
        driver.execute_script("arguments[0].click();", submit)
        time.sleep(1)

    except TimeoutException:
        print("Page Loading took too much time!")


def main():

    ALL_PROXIES = get_proxies()
    # --- YOU ONLY NEED TO CARE FROM THIS LINE ---
    # creating new driver to use proxy
    pd = proxy_driver(ALL_PROXIES)

    # code must be in a while loop with a try to keep trying with different proxies
    running = True

    while running:
        try:
            firstsite(pd)
            secondsite(pd)
            new = ALL_PROXIES.pop()
            pd.close()
            # reassign driver if fail to switch proxy
            pd = proxy_driver(ALL_PROXIES)
            print("--- Switched proxy to: %s" % new)
            time.sleep(1)
            if len(ALL_PROXIES) == 0:
                running = False
        except:
            new = ALL_PROXIES.pop()
            #pd.close()
            # reassign driver if fail to switch proxy
            pd = proxy_driver(ALL_PROXIES)
            print("--- Switched proxy to: %s" % new)
            time.sleep(1)
            if len(ALL_PROXIES) == 0:
                running = False

    pd.close()
if __name__ == "__main__":
    main()