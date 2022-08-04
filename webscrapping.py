#  import all the libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

#  define path to chrome driver & website url
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.edmunds.com/cars-for-sale-by-owner/") #change the url accordding to your need.

'''  "Scrapper()" This Function Fetch the name of all cars on the page and made them 
available to be clicked and once the specific Car is open
then we fetch all the required information about the car and append them
 on a dictionary so it can be converted into data frame and  write it to 
 Ms excel and then move back to previous page and open the next car 
 and this process  will end when all the cars on the page is done and then 
 finally we move our information into excel'''

def scrapper():
    driver.execute_script("window.scrollTo(0,250);")
    driver.maximize_window()
    href_list = driver.find_elements_by_class_name("usurp-inventory-card-vdp-link")
    href_list = [href.get_attribute('aria-label') for href in href_list if href.get_attribute('aria-label') is not None]
    dict_for_xl ={"Name":[], "Price":[], "VIN":[], "Vehicle_Summary":[]}
    for i in range(len(href_list)):
        clicked = driver.find_element_by_link_text(href_list[i]).click()
        time.sleep(3)
        name = driver.find_element_by_css_selector(".not-opaque.text-black.d-inline-block.mb-0.size-24").text
        vin_number = driver.find_element_by_css_selector("span[class='mr-1']").text
        price = driver.find_element_by_css_selector("span[data-test='vdp-price-row']").text
        summary = driver.find_element_by_css_selector(".mb-0.max-width.text-capitalize.pl-1_25.pl-md-0.pl-lg-1_25.row").text
        dict_for_xl["Name"].append(name)
        dict_for_xl["Price"].append(price)
        dict_for_xl["VIN"].append(vin_number)
        dict_for_xl["Vehicle_Summary"].append(summary)
        driver.back()
        time.sleep(18)
    driver.quit()
    df = pd.DataFrame(dict_for_xl,columns=['Name','Price','VIN','Vehicle_Summary'])
    df.to_excel(r'F:\py programs\web scrapping\findings.xlsx',index=False)


'''Zip_code()  This  function searches for the zip code field clear the default 
 value and ask user to enter their desired zip code and filter out
 the desired results'''

def Zip_code(zip_code):
    zip_search = driver.find_element_by_name("zip")
    driver.execute_script("arguments[0].value= '' ",zip_search)
    zip_search.send_keys(zip_code)
    zip_search.send_keys(Keys.RETURN)


'''Radius()  This function  target the Radius selector field ask user
to enter their  desired Radius match them with the corresponding
range to set movements and enters for the given range and filter out
the results'''

def Radius(radius_val):
    radius_selector=driver.find_element_by_id("search-radius-range-min")
    my_dict = {10:2, 25:1, 50:8, 75:1, 100:2, 200:3, 500:4}
    for key, value in my_dict.items():
        if key == radius_val:
            comp_val=value

    if radius_val> 50:
        radius_selector.send_keys(Keys.ARROW_RIGHT*comp_val)
        radius_selector.send_keys(Keys.ENTER)
    elif radius_val < 50:
        radius_selector.send_keys(Keys.ARROW_LEFT*comp_val)
        radius_selector.send_keys(Keys.ENTER)
    elif radius_val == 50:
        radius_selector.send_keys(Keys.ENTER)


'''This is our point from where the program started to get execute 
and here we have call all of our functions'''
# if __name__ == '__main__':
    # Radius(radius_val=int(input("Enter Radius: ")))
    # Zip_code(zip_code=input("Enter Zip code: "))
    # scrapper()