import requests
import json
import time
from config import INFO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
start_time = time.time()
URL = 'https://www.supremenewyork.com/mobile_stock.json'
r = requests.get(URL)
products = json.loads(r.text)['products_and_categories']
for product in products[INFO['category']]:
    if INFO['product'] in product['name']:
        id = product['id']
        print(product['name'], id)
        # AKA product found!!
style = 'https://www.supremenewyork.com/shop/' + str(id) + '.json'
r = requests.get(style)
styles = json.loads(r.text)['styles']
for item in styles:
    if INFO['color'] in item['name']:
        for size in item['sizes']:
            if INFO['size'] == size['name']:
                styleID = size['id']
print("--- %s seconds ---" % (time.time() - start_time))
driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://www.supremenewyork.com/shop/' + str(id))
print(styleID)
#GET THE PROPER SIZE
select = Select(driver.find_element_by_id('s'))
select.select_by_value(str(styleID))
# driver.find_element_by_name('qty').send_keys('1')
driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
# webdriver wait
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cart > a.button.checkout"))).click()
driver.find_element_by_css_selector('#order_billing_name').send_keys(INFO['name'])
driver.find_element_by_css_selector('#order_email').send_keys(INFO['email'])
driver.find_element_by_name('order[tel]').send_keys(INFO['phone'])
driver.find_element_by_css_selector('#bo').send_keys(INFO['address'])
driver.find_element_by_css_selector('#order_billing_zip').send_keys(INFO['zip'])
driver.find_element_by_css_selector('#order_billing_city').send_keys(INFO['city'])
driver.find_element_by_name('order[billing_country]').send_keys('USA')
driver.find_element_by_css_selector('#rnsnckrn').send_keys(INFO['number'])
#ccv field 
driver.find_element_by_css_selector('#orcer').send_keys(INFO['ccv'])
#credit card month formatted 09 = Sept
driver.find_element_by_name('credit_card[month]').send_keys(INFO['month'])
# Credit Card Year 1 = 2010 2 = 2021 3 = 2022 4 = 2023 etc...
driver.find_element_by_css_selector('#credit_card_year > option:nth-child(4)').click()
# click accept
driver.find_element_by_css_selector('#cart-cc > fieldset > p > label > div').click()
#process payment
driver.find_element_by_name('commit').click()
print("--- %s seconds ---" % (time.time() - start_time))