from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import os




def noon_scrape(link):
    #======================================= Outer try-except start ===========================================================
    try:    
        service = Service(ChromeDriverManager(driver_version="144.0.7559.110").install())          # driver_version="144.0.7559.110"
        browser = webdriver.Chrome(service=service)

        # To open and download website only:
        browser.get(link)
        time.sleep(3)

        # scrape watchs name by using beautiful-soup:
        watchs_list = browser.find_elements('class name', 'ProductDetailsSection-module-scss-module__Y6u1Qq__wrapper')

        #======================================= Inner try-except start ======================================================
        try:
            products_list = []
            for watch in watchs_list:
                html_code = watch.get_attribute("outerHTML")            # return an html code for dynamic pages
                soup = BeautifulSoup(html_code, 'lxml')                 # parsing operation

                watch_name = soup.find('h2', {'data-qa': 'plp-product-box-name'}).text.strip()
                watch_price = soup.find('strong', class_='Price-module-scss-module__q-4KEG__amount').text.strip()

                rate = soup.find('div', class_='RatingPreviewStar-module-scss-module__zCpaOG__textCtr')
                watch_rate = rate.text.strip() if rate else "Undefined"

                old_price = soup.find('span', class_='Price-module-scss-module__q-4KEG__oldPrice')
                watch_oldprice = old_price.text.strip() if old_price else "Undefined"

                percent = soup.find('span', class_="PriceDiscount-module-scss-module__6h-Fca__discount")
                sale_percent = percent.text.strip().split(' ')[0] if percent else "No Sale"
                
                # assign items on products list:
                products_list.append({
                    "Details": watch_name, "Price": watch_price, "Old Price": watch_oldprice, "Sale Percent": sale_percent, "Rate": watch_rate
                })

               
            print('All function operations done ✅....')
            return products_list
            

        except Exception as e:
            print(f'something went wrong on inernal try-except ==> {e}')
        #======================================= Inner try-except end ======================================================

    except Exception as e:
        print(f'Something went wrong as ==> {e}')
    #============================================ Outer try-except end ======================================================
    

#============================================================================================================================
#============================================================================================================================
#========================================== Global scope to loop all pages & fill excel file ................................
pages_number = 47
product = "smart watch"
all_products_list = []
for i in range(pages_number):
    url = f'https://www.noon.com/egypt-en/search/?page={i}&q={product}'
    all_products_list += noon_scrape(url)


df = pd.DataFrame(all_products_list)
try:
    file_name = r'SmartWatchsNoon.xlsx'
    df.to_excel(file_name, index=False)
    print('Scraping Done ✅')
    time.sleep(2)
    os.startfile(file_name)
except:
    print('Saving error !!')
