from requests_download import download
import lxml.html,os,json,requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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
from tkinter import *
from tkinter import messagebox

def uploadinfo(driver,HOME):
    delay = 5
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'content_right_top')))
        print("AddaListing Page is ready!")
        time.sleep(3)

        #City input

        CityButtons = driver.find_elements_by_css_selector("button.btn.dropdown-toggle.bs-placeholder.btn-default")
        for id,CityButton in enumerate(CityButtons):
            if id == 0:
                # City input
                CityText = HOME["label2"]
                driver.execute_script("arguments[0].click();", CityButton)
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, CityText)))
                    element.click()
                    time.sleep(2)
                except NoSuchElementException as e:
                    time.sleep(1)
            if id == 1:
                # Neighborhood input
                NeiHood = HOME["label8"].split(" ")
                driver.execute_script("arguments[0].click();", CityButton)
                try:
                    elements = driver.find_elements_by_css_selector("ul.dropdown-menu.inner")
                    for idx,elem in enumerate(elements):
                        if idx == 3:
                            liList = elem.find_elements_by_tag_name("li")
                            for litag in liList:
                                el = litag.find_elements_by_class_name("text")
                                hood = str(el[0].text)
                                if len(NeiHood) > 1:
                                    if (hood.find(NeiHood[0]) != -1) and (hood.find(NeiHood[1]) != -1):
                                        driver.execute_script("arguments[0].click();", el[0])
                                        break
                                    elif hood.find(NeiHood[0]) != -1:
                                        driver.execute_script("arguments[0].click();", el[0])
                                        break
                                elif len(NeiHood) == 1:
                                    if hood.find(NeiHood[0]) != -1:
                                        driver.execute_script("arguments[0].click();", el[0])
                                        break
                except NoSuchElementException as e:
                    time.sleep(1)

        #Address input
        Address = driver.find_element_by_id("Address")
        Address.send_keys(HOME["label0"])

        #ZipCodp input
        ZipCode = driver.find_element_by_id("ZipCode")
        ZipCode.send_keys(HOME["label4"])

        #mlsnum input
        mlsnum = driver.find_element_by_id("MlsNumber")
        mlsnum.send_keys(HOME["MLS"])

        price = driver.find_element_by_id("Price")
        price.send_keys(HOME["List:"])

        #get images name and upload images
        mypath = os.getcwd() + "/images/" + HOME["MLS"]
        imgs = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        imgurl = []
        for img in imgs:
            imgurl.append(mypath + "/" + img)
        #imgurl = ["E://task72//home//1.jpg","E://task72//home//2.jpg","E://task72//home//3.jpg","E://task72//home//4.jpg","E://task72//home//5.jpg"]
        for img in imgurl:
            uploadbutton = driver.find_element_by_id("AddPhotoBtn")
            webdriver.ActionChains(driver).move_to_element(uploadbutton).click(uploadbutton).perform()
            fileupload = driver.find_element_by_css_selector("span.button.button-white.btn-add-photo.fileinput-button")
            inputfile = fileupload.find_element_by_css_selector("input")
            inputfile.send_keys(img)
        buttonbar = driver.find_element_by_css_selector("div.row.fileupload-buttonbar")
        butto = buttonbar.find_element_by_css_selector("button.button.start")
        driver.execute_script("arguments[0].click();", butto)


        #description input
        driver.switch_to.frame(driver.find_element_by_id("Description_ifr"))
        description = driver.find_element_by_id("tinymce")
        description.send_keys(HOME["Client Remks:"] + "\n" + HOME["Extras:"])
        driver.switch_to.default_content()


        Type = Select(driver.find_element_by_id('BuildingDetails_Type'))
        Type.select_by_value('1')
        time.sleep(1)

        StyleText = HOME["label15"]
        Style = Select(driver.find_element_by_id('residentialSubTypes'))
        if (StyleText.find("Condo Apt") != -1):
            Style.select_by_value("1")
        elif (StyleText.find("Detached") != -1) or (StyleText.find("Duplex") != -1) or (StyleText.find("Fourplex") != -1) or (StyleText.find("Semi-Detached") != -1) or (StyleText.find("Triplex") != -1) or (StyleText.find("Multiplex") != -1):
            Style.select_by_value("4")
        elif (StyleText.find("Att/Row/Townhouse") != -1) or (StyleText.find("Condo Townhouse") != -1):
            Style.select_by_value("7")

        Builtext = HOME["Apx Age:"]
        if Builtext != "":
            Txt = Builtext.split("-")
            if Txt[0].isdigit():
                YearBuilt = driver.find_element_by_id("BuildingDetails_YearBuilt")
                YearBuilt.send_keys(int(Txt[0]))

        SizeTxt = HOME["Apx Sqft:"]
        if SizeTxt != "":
            Txt = SizeTxt.split("-")
            Size = driver.find_element_by_id("BuildingDetails_Size")
            Size.send_keys(int(Txt[1]))

        RoomCount = eval(HOME["Bedrooms:"])
        Bedroom = driver.find_element_by_id("BuildingDetails_Bedrooms")
        Bedroom.send_keys(RoomCount)

        Bathroom = driver.find_element_by_id("BuildingDetails_Bathrooms")
        Bathroom.send_keys(RoomCount)

        if "Tot Pk Spcs:" in HOME:
            GarageStalls = driver.find_element_by_id("BuildingDetails_GarageStalls")
            GarageStalls.send_keys(int(float(HOME["Tot Pk Spcs:"])))
        elif "Tot Prk Spcs:" in HOME:
            GarageStalls = driver.find_element_by_id("BuildingDetails_GarageStalls")
            GarageStalls.send_keys(int(float(HOME["Tot Prk Spcs:"])))

        GarageType = Select(driver.find_element_by_id('BuildingDetails_GarageType'))
        GarageType.select_by_value("1")

        if HOME["Basement:"] != "None":

            Basement = Select(driver.find_element_by_id('BuildingDetails_HasBasement'))
            Basement.select_by_value("True")

            BasementType = Select(driver.find_element_by_id('basementTypes'))
            BaseText = HOME["Basement:"]
            if BaseText.find("Crawl Space") != -1:
                BasementType.select_by_value("1")
            elif BaseText.find("Full") != -1:
                BasementType.select_by_value("2")
            elif (BaseText.find("Half") != -1) or (BaseText.find("Part Bsmnt") != -1) or (BaseText.find("Part Fin") != -1):
                BasementType.select_by_value("3")
            elif (BaseText.find("Other") != -1) or (BaseText.find("Unfinished") != -1):
                BasementType.select_by_value("4")
            elif (BaseText.find("Walk Up") != -1) or (BaseText.find("W/O") != -1) or (BaseText.find("Fin W/O") != -1) or (BaseText.find("Sep Entrance") != -1) or (BaseText.find("Finished") != -1) or (BaseText.find("Apartment") != -1):
                BasementType.select_by_value("5")
        # LoT input
        if "Lot:" in HOME:
            LoTarray = HOME["Lot:"].split(" ")
            try:
                LotWidth = driver.find_element_by_id("Lot_DimensionWidth")
                LotWidth.send_keys(LoTarray[0])
            except NoSuchElementException as e:
                time.sleep(1)
            try:
                LotLength = driver.find_element_by_id("Lot_DimensionLength")
                LotLength.send_keys(LoTarray[2])
            except NoSuchElementException as e:
                time.sleep(1)
            try:
                LotUnit = Select(driver.find_element_by_id('Lot_LotMeasurementUnit'))
                if LoTarray[3].lower() == "feet":
                    LotUnit.select_by_value("0")
                elif LoTarray[3].lower() == "inches":
                    LotUnit.select_by_value("1")
                elif LoTarray[3].lower() == "meters":
                    LotUnit.select_by_value("2")

            except NoSuchElementException as e:
                time.sleep(1)
        #Appliances checkbox click

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[1].Selected")
            driver.execute_script("arguments[0].click();",elem)
        except NoSuchElementException as e:
            time.sleep(1)

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[4].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[5].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[11].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[15].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[17].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[18].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        try:
            elem = driver.find_element_by_name("Features.AppliancesFeatures[20].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        #Heating find element and checkbox click
        try:
            elem = driver.find_element_by_name("Features.HeatingFeatures[2].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

    #Cooling find element and checkbox click
        try:
            elem = driver.find_element_by_name("Features.CoolingFeatures[3].Selected")
            driver.execute_script("arguments[0].click();", elem)
        except NoSuchElementException as e:
            time.sleep(1)

        #Extra Features find elements and checkbox click
        if "Balcony:" in HOME:
            try:
                text = HOME["Balcony:"]
                if text == "Open":
                    elem = driver.find_element_by_name("Features.ExtraFeatures[1].Selected")
                    driver.execute_script("arguments[0].click();", elem)
            except NoSuchElementException as e:
                time.sleep(1)
        if "Bldg Amen:" in HOME:
            try:
                BldgText = HOME["Bldg Amen:"]
                if BldgText.find("Exercise") != -1:
                    elem = driver.find_element_by_name("Features.ExtraFeatures[7].Selected")
                    driver.execute_script("arguments[0].click();", elem)
                elif BldgText.find("Amen:Concierge") != -1:
                    elem = driver.find_element_by_name("Features.ExtraFeatures[20].Selected")
                    driver.execute_script("arguments[0].click();", elem)

            except NoSuchElementException as e:
                time.sleep(1)
        if "Locker:" in HOME:
            try:
                text = HOME["Locker:"]
                if text != "None":
                    elem = driver.find_element_by_name("Features.ExtraFeatures[22].Selected")
                    driver.execute_script("arguments[0].click();", elem)
            except NoSuchElementException as e:
                time.sleep(1)
        if "Park/Drive" in HOME:
            try:
                text = HOME["Park/Drive:"]
                if text != "None":
                    elem = driver.find_element_by_name("Features.ExtraFeatures[5].Selected")
                    driver.execute_script("arguments[0].click();", elem)
            except NoSuchElementException as e:
                time.sleep(1)

        time.sleep(100)
        #submit button click
        buttonbar = driver.find_element_by_class_name("btn-section")
        savebutton = buttonbar.find_element_by_css_selector("button.button")
        driver.execute_script("arguments[0].click();", savebutton)


        time.sleep(3)
        driver.close()
    except TimeoutException:
        print("Loading AddAListing Page took too much time!")
        time.sleep(3)
        driver.close()




def WebsiteLoading(HOME,MAIL,PASSWD):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches",
                                    ["ignore-certificate-errors", "safebrowsing-disable-download-protection",
                                     "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery");
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path="D:/chromedriver.exe",chrome_options=chrome_options)
    driver.delete_all_cookies()
    item_url = "https://www.point2homes.com/Account/AddAListing"
    driver.get(item_url)
    delay = 5  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'Username')))
        print("login Page is ready!")
        username = driver.find_element_by_id("Username")
        password = driver.find_element_by_id("Password")

        username.send_keys(MAIL)
        password.send_keys(PASSWD)
        button = driver.find_element_by_class_name("withanimation")
        button.click()
        time.sleep(5)
        uploadinfo(driver,HOME)
    except TimeoutException:
        print("Loading login page took too much time!")
        time.sleep(3)
        driver.close()



def KijiAddLocation(driver,HOME):
    #BuildingName input
    try:
        BuildingName = driver.find_element_by_id("location_new_buildingName")
        BuildingName.send_keys(HOME["Address_0"])
    except NoSuchElementException as e:
        time.sleep(1)

    #Email input
    AddMail = driver.find_element_by_id("s2id_email_user")
    AddMail.click()
    try:
        LocDiv = driver.find_element_by_id("select2-drop")
        maillists = LocDiv.find_elements_by_class_name("select2-result-label")
        for mail in maillists:
            if mail.text == "UNITTOGO (info@unittogo.com)":
                mail.click()
                break
    except NoSuchElementException as e:
        time.sleep(1)
    AddMail.click()
    try:
        LocDiv = driver.find_element_by_id("select2-drop")
        maillists = LocDiv.find_elements_by_class_name("select2-result-label")
        for mail in maillists:
            if mail.text == "Tara OKUYUCU (tara.o@remaxhallmark.com)":
                mail.click()
                break
    except NoSuchElementException as e:
        time.sleep(1)

    #Address input
    try:
        Address = driver.find_element_by_id("location_new_address")
        Address.send_keys(HOME["Address_0"])
    except NoSuchElementException as e:
        time.sleep(1)

    # City input
    try:
        Address = driver.find_element_by_id("location_new_city")
        Citytxt = str(HOME["label7"]).split(" ")
        Address.send_keys(Citytxt[0])
    except NoSuchElementException as e:
        time.sleep(1)
    # Province input
    Location = driver.find_element_by_id("s2id_location_new_province")
    Location.click()
    try:
        LocDiv = driver.find_element_by_id("select2-drop")
        LocSearch = LocDiv.find_element_by_class_name("select2-input")
        LocSearch.send_keys(HOME["label3"])
        LocSearch.send_keys(Keys.ENTER)
    except NoSuchElementException as e:
        time.sleep(1)

    # PostCode input
    try:
        PostCode = driver.find_element_by_id("location_new_postalCode")
        PostCode.click()
        #driver.execute_script("arguments[0].click();", PostCode)
        PostCode.send_keys(HOME["label4"])
        '''for charter in HOME["Address_4"]:
            PostCode.click()
            PostCode.send_keys(charter)
        '''
    except NoSuchElementException as e:
        time.sleep(1)
    # Kijiji Location input

    KijLocal = driver.find_element_by_id("s2id_location_new_kijijiLocationId")
    KijLocal.click()
    try:
        LocDiv = driver.find_element_by_id("select2-drop")
        LocSearch = LocDiv.find_element_by_class_name("select2-input")
        LocSearch.send_keys(HOME["Address_2"])
        LocSearch.send_keys(Keys.ENTER)
    except NoSuchElementException as e:
        time.sleep(1)
    #Save Button Click
    SaveButton = driver.find_element_by_id("btn_Save")
    SaveButton.click()
    time.sleep(3)
    #uploadinfo(driver,HOME)


def KijiUploadinfo(driver,HOME):
    delay = 5
    try:


        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'locationContainer')))
        print("Ads Page is ready!")
        time.sleep(3)

        #Location click
        Location = driver.find_element_by_id("s2id_real_estate_ad_location")
        Location.click()
        try:
            LocDiv = driver.find_element_by_id("select2-drop")
            LocSearch = LocDiv.find_element_by_class_name("select2-input")
            LocSearch.send_keys(HOME["Address_0"])
            LocSearch.send_keys(Keys.ENTER)
            Local = driver.find_element_by_class_name("select2-chosen")
            if Local.text == "Select Location":
                driver.get("http://re.kit.kijiji.ca/en/location/new?returnurl=true")
                KijiAddLocation(driver,HOME)
                #pass

        except NoSuchElementException as e:
            time.sleep(1)

        #Title input
        try:
            Title = driver.find_element_by_id("real_estate_ad_title")
            Title.send_keys(HOME["MLS"])
        except NoSuchElementException as e:
            time.sleep(1)

        #description input
        try:
            driver.switch_to.frame(driver.find_element_by_id("real_estate_ad_description_ifr"))
            description = driver.find_element_by_id("tinymce")
            description.send_keys(HOME["Client Remks:"])
            driver.switch_to.default_content()
        except NoSuchElementException as e:
            time.sleep(1)

        #Additional Email
        try:
            AddEmail = driver.find_element_by_id("s2id_email_user")
            EmailAdd = AddEmail.find_element_by_tag_name("input")
            EmailAdd.send_keys("UNITTOGO (info@unittogo.com)")
            EmailAdd.send_keys(Keys.ENTER)
            EmailAdd.send_keys("Tara OKUYUCU (tara.o@remaxhallmark.com)")
            EmailAdd.send_keys(Keys.ENTER)
        except NoSuchElementException as e:
            time.sleep(1)

        #Listing Category
        try:
            CatList = Select(driver.find_element_by_id("real_estate_unitType"))
            if HOME["label15"].find("Condo Apt") == -1:
                CatList.select_by_value("35")
            else:
                CatList.select_by_value("643")
        except NoSuchElementException as e:
            time.sleep(1)

        #Bedrooms input
        Bedrooms = driver.find_element_by_id("s2id_attributes_attribs_0_selects_172")
        BedChoose = Bedrooms.find_element_by_class_name("select2-chosen")
        BedChoose.click()
        try:
            BedDiv = driver.find_element_by_id("select2-drop")
            BedSearch = BedDiv.find_element_by_class_name("select2-input")
            BedCount = str(HOME["Bedrooms:"]).split("+")
            if int(BedCount[0]) == 0:
                BedSearch.send_keys("Bachelor/Studio")
                BedSearch.send_keys(Keys.ENTER)
            elif int(BedCount[0]) > 3:
                BedSearch.send_keys("4")
                BedSearch.send_keys(Keys.ENTER)
            else:
                BedSearch.send_keys(BedCount[0])
                BedSearch.send_keys(Keys.ENTER)
        except NoSuchElementException as e:
            time.sleep(1)
        #Bathrooms input
        try:
            Bathrooms = driver.find_element_by_id("s2id_attributes_attribs_0_selects_173")
            BathChoose = Bathrooms.find_element_by_class_name("select2-chosen")
            BathChoose.click()
            try:
                BathDiv = driver.find_element_by_id("select2-drop")
                BathSearch = BathDiv.find_element_by_class_name("select2-input")
                WashCount = int(eval(HOME["Washrooms:"]))
                if WashCount > 5:
                    BathSearch.send_keys("6")
                    BathSearch.send_keys(Keys.ENTER)
                else:
                    BathSearch.send_keys(HOME["Washrooms:"])
                    BathSearch.send_keys(Keys.ENTER)
            except NoSuchElementException as e:
                time.sleep(1)
        except NoSuchElementException as e:
            time.sleep(1)

        #Price input
        try:
            price = driver.find_element_by_id("real_estate_ad_price")
            HomePrice = re.sub('[^A-Za-z0-9]+', '', HOME["List:"])
            price.send_keys(HomePrice)
        except NoSuchElementException as e:
            time.sleep(1)

        #Images Upload
        mypath = os.getcwd() + "/images/" + HOME["MLS"]
        imgs = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        imgurl = []
        for img in imgs:
            imgurl.append(mypath + "/" + img)
        for img in imgurl:

            fileupload = driver.find_element_by_css_selector("span.btn.btn-success.fileinput-button")
            inputfile = fileupload.find_element_by_css_selector("input")
            inputfile.send_keys(img)
        time.sleep(30)
        # Save Button Click
        InactButton = driver.find_element_by_name("save-inactive")
        InactButton.click()

        time.sleep(3)
        driver.close()
    except TimeoutException:
        print("Ads Page Loading took too much time!")





def KijiOpenWebsite(HOME,MAIL,PASSWD):
    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-data-dir={}".format(userProfile))
    chrome_options.add_experimental_option("excludeSwitches",
                                    ["ignore-certificate-errors", "safebrowsing-disable-download-protection",
                                     "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery");
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path="D:/chromedriver.exe",chrome_options=chrome_options)
    driver.delete_all_cookies()
    item_url = "http://re.kit.kijiji.ca/en/unit/add"
    driver.get(item_url)
    delay = 5  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'username')))
        print("Page is ready!")
        username = driver.find_element_by_id("username")
        password = driver.find_element_by_id("password")

        username.send_keys(MAIL)
        password.send_keys(PASSWD)

        button = driver.find_element_by_id("_submit")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'tab1')))
        print("DashBoard Page is ready!")
        time.sleep(1)

        # New Ad Button Click
        try:
            NewAd = driver.find_element_by_css_selector("a.pull-right.btn.btn-default.add-edit-unit")
            driver.execute_script("arguments[0].click();", NewAd)

        except:
            print("No Adds Button")

        KijiUploadinfo(driver,HOME)
    except TimeoutException:
        print("Kiji Login Page Loading took too much time!")




def StartMain(scrapingurl,mail,passwod,mail1,passwod1):
    cookiesList = [{
	    '_ga': 'GA1.2.1700526595.1562353772',
	    'DG_IID': '1F0A32E9-312D-3A37-8C76-FD423D7DD7CB',
	    'DG_UID': 'E6B29B47-0D07-39EA-A8F3-1AB8491A4715',
	    'DG_ZID': '37A2504E-56CB-300B-B808-EB880195D761',
	    'DG_ZUID': '2B4EFECC-4336-3C79-BCC7-A7C324BC319E',
	    'DG_HID': '64CD7855-FFF4-3BFA-8377-3EE62110EDEB',
	    'DG_SID': '112.72.98.74:OmLiYC7xWc8CPD6H/+kymRTCrOSypamOScLOHFnVals',
	    'S': '0heemi1em5jbqojqub42ixu3',
	    'Qr1B4j3mrGOWWlAIrB7u5C7QWf8G4A@@': 'v1RvQYgw@@ZNh',
	    '_gid': 'GA1.2.2050803316.1563099665',
	    '_gat': '1',
	    },{
        '_ga': 'GA1.2.1700526595.1562353772',
        'DG_IID': '1F0A32E9-312D-3A37-8C76-FD423D7DD7CB',
        'DG_UID': 'E6B29B47-0D07-39EA-A8F3-1AB8491A4715',
        'DG_ZID': '27F459B7-78F4-3C41-829C-3D4510B8B951',
        'DG_ZUID': '5854C0B3-CA7E-3481-980A-E0D020504B2D',
        'DG_HID': '1130CA69-827F-3D85-937F-42EC972B6C64',
        'DG_SID': '112.72.98.74:OmLiYC7xWc8CPD6H/+kymRTCrOSypamOScLOHFnVals',
        'S': 'gfo3tjlodpjpe4ughyk32rqo',
        'Qr1B4j3mrGOWWlAIrB7u5C7QWf8G4A@@': 'v1RPQYgw@@SRx',
        '_gid': 'GA1.2.1078663764.1562455209',
    },{
        'S': '4b4lnmpmj4hvbzxt5cqshfn0',
        'Qr1B4j3mrGOWWlAIrB7u5C7QWf8G4A@@': 'v1T/QYgw@@1bn',
        'DG_IID': '7E32FE40-F925-36CB-A97F-3585432EACC1',
        'DG_UID': 'A3E172C9-2C5A-340B-8A0B-C508599D120A',
        'DG_ZID': 'F469F273-DE68-3459-9B68-2E21D8CFF660',
        'DG_ZUID': '3AE599EF-6EDF-3CA9-9EA9-810D8021112A',
        'DG_HID': '46968B3C-425D-3F2C-A43F-B27DEC81C6DD',
        'DG_SID': '171.236.93.85:Z+uesN5AOoUjpB5Ki4IKyjqkKSw8zy0i5snXaiRSh30',
        '_ga': 'GA1.2.1757745723.1562341012',
        '_gid': 'GA1.2.1190884154.1562341012',
    },{
        '_ga': 'GA1.2.1700526595.1562353772',
        'DG_IID': '457A4A4E-4102-3439-9F48-FD3A8823AF10',
        'DG_UID': '440AF410-834A-3F82-B1B5-FBADE7ACA144',
        'DG_ZID': '27F459B7-78F4-3C41-829C-3D4510B8B951',
        'DG_ZUID': '5854C0B3-CA7E-3481-980A-E0D020504B2D',
        'DG_HID': '1130CA69-827F-3D85-937F-42EC972B6C64',
        'DG_SID': '112.72.98.74:OmLiYC7xWc8CPD6H/+kymRTCrOSypamOScLOHFnVals',
        'S': 'c4rs2tee41nm2vr0nev3rwde',
        'A': 'D1F7D6A15C8DE6302987AA17C881E14F7C7C326616633E001FE691317EE4C43B49DC50D4E69F27EDEE6D1BC32883FB6EDD57D2CFDC7FAD3868E645EC975A5BC933CD7727D2D4D88079F1E3FACCACFC14CB511604D2AFB9AF2EA7DB8914EA5CB611CCC9FBEAD13ECA1C7CB8386CFDEB28D6F4C5A1D0740CF517D4F36FA53B0CD632A4C1852D9AB845F01E15561921AE6618425E50B51CAE7CD37A0CEF36203778',
        '_gid': 'GA1.2.1807101646.1562724451',
        'Qr1B4j3mrGOWWlAIrB7u5C7QWf8G4A@@': 'v1R/QYgw@@Y+Q',
    }]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    params = (
        ('Key', 'ce8c842e8e1846a487d9112b1a5a04e8'),
        ('App', 'TREB'),
    )

    total=muc=moi=cu=0
    duongdan="./"

    if not os.path.exists(duongdan+"images"):
        os.makedirs(duongdan+"images")
        #os.system("chmod -R 777 "+duongdan+"images")
    if not os.path.exists(duongdan+"data"):
        os.makedirs(duongdan+"data")
        #os.system("chmod -R 777 "+duongdan+"data")

    cookies = random.choice(cookiesList)
    response = requests.get(scrapingurl, headers=headers, cookies=cookies)

    strhtml = response.text
    html = lxml.html.fromstring(strhtml)
    Data = html.xpath('//div[@class="formitem form viewform"]')
    if len(Data) != 0:
        for row in Data:
            total = total+1
            item = {}
            dl = row.xpath('.//div[@class="formitem formgroup horizontal"][1]/div[1]/span[1]/span/text()')
            MLS = str(dl[1])
            item['MLS'] = MLS
            dulieu = row.xpath('.//span[@class="formitem formfield"]//span/text()')
            for i in range(0,5,1):
                item['Address_'+str(i)]=dulieu[i]
            dt=row.xpath('.//span[@class="formitem formfield"]')
            for idx,rs in enumerate(dt):
                if(rs.xpath('./label')):
                    if(rs.xpath('./span/text()')):
                        item[str(rs.xpath('./label/text()')[0])] = rs.xpath('./span/text()')[0]
                    else:
                        item[str(rs.xpath('./label/text()')[0])] = ""
                else:
                    if (rs.xpath('./span/text()')):
                        item["label" + str(idx)] = rs.xpath('./span/text()')[0]
                    else:
                        item["label" + str(idx)] = ""

            filename = "data/"+MLS+".json"
            if os.path.exists(filename):
                cu = cu + 1
                with open(filename) as f:
                    item = json.load(f)
                    WebsiteLoading(item,mail,passwod)
                    KijiOpenWebsite(item,mail1,passwod1)
            else:
                moi = moi + 1
                with open(filename, 'w') as outfile:
                    json.dump(item, outfile)
                    print("Save json file: " + MLS)
                Anh = row.xpath('.//div[@class="imageset_container "]//img/@data-multi-photos')
                anh = json.loads(Anh[0])
                dlanh = anh['multi-photos']
                i=1
                if not os.path.exists("images/" + MLS):
                    os.makedirs(duongdan + "/images/" + MLS)
                    # os.system("chmod -R 777 images/"+MLS)
                    print("Images download for.... :" + MLS)
                for dla in dlanh:
                    imgf=MLS+"_"+str(i)+".jpg"
                    imgurl=str(dla['url']).replace('&size=250','')
                    if not os.path.exists("images/"+MLS+"/"+imgf):
                        download(imgurl,"images/"+MLS+"/"+imgf)
                    i=i+1
                WebsiteLoading(item,mail, passwod)
                KijiOpenWebsite(item,mail1,passwod1)
            print("Uploading End: " + item["MLS"])

        print("Uploading End")
        messagebox.showinfo("Success", "Uploading End")
    else:
        print("Wrong Url")
        messagebox.showwarning("Warning","Incorrect Url~")
        textBox.delete('1.0', END)


def retrieve_input():
    firstemail = entry1.get()
    firstpass = entry2.get()
    secondemail = entry3.get()
    secondpass = entry4.get()
    if firstemail !="" and firstpass != "" and secondemail != "" and secondpass != "":
        buttonCommit.config(state="disabled")
        inputValue = textBox.get("1.0", "end-1c")
        print(inputValue)
        if (str(inputValue).find("https:") != -1) or (str(inputValue).find("http:") != -1):
            StartMain(inputValue,firstemail,firstpass,secondemail,secondpass)
        else:
            messagebox.showwarning("Warning", "Please... Input correct Link~")
            textBox.delete('1.0', END)

        buttonCommit.config(state="normal")
    else:
        messagebox.showwarning("Warning","Please... Input All emails and Password")


if __name__ == "__main__":

    root = Tk()
    root.option_add("*Button.Background", "yellow")
    root.option_add("*Button.Foreground", "black")
    root.title('The Uploading Estate')
    root.geometry("700x500")  # You want the size of the app to be 500x500
    root.resizable(0, 0)

    frame = Frame(root)
    Label1 = Label(frame, text='point2homes Email:')
    Label1.grid(row=0, sticky=E)

    entry1 = Entry(frame, bd=5)
    entry1.grid(row=0, column=1)

    Label2 = Label(frame, text='point2homes Password: ')
    Label2.grid(row=0,column=2, sticky=E)

    entry2 = Entry(frame, bd=5)
    entry2.grid(row=0, column=3)

    Label3 = Label(frame, text='re.kit.kijiji.ca Email:')
    Label3.grid(row=1, sticky=E)

    entry3 = Entry(frame, bd=5)
    entry3.grid(row=1, column=1)

    Label4 = Label(frame, text='re.kit.kijiji.ca Password: ')
    Label4.grid(row=1,column=2, sticky=E)

    entry4 = Entry(frame, bd=5)
    entry4.grid(row=1, column=3)

    frame.pack()

    textBox = Text(root, height=20, width=100)
    textBox.pack()
    buttonCommit = Button(root, height=10, width=40, text="Uploading",background = 'blue', foreground = "white",
                          command=lambda: retrieve_input())
    buttonCommit.pack()
    mainloop()
