from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

#Step 1 - Scrape the links, addresses, and prices of the rental properties
URL = "https://appbrewery.github.io/Zillow-Clone/"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,uk;q=0.7"
}

response = requests.get(URL, headers=header)
page = response.text

# Create a list of all the links on the page using a CSS Selector
soup = BeautifulSoup(page, 'html.parser')
addresses = soup.find_all('address')
prices = soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')
links = soup.find_all('a', class_='property-card-link', href=True)
addresses_list = [address.text.strip() for address in addresses]
prices_list = [price.text.split('+')[0].replace('/mo', '') for price in prices]
links_list = [link['href'] for link in links]

# Step 2 - automate form filling with selenium
# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(
    "https://docs.google.com/forms/d/e/1FAIpQLSdOMP5PXGTyEaeRVrBnnD4KicjBLpTxFr7QVmU9cMKAnS-1Cw/viewform?usp=sf_link")

for i in range(0, len(addresses_list) - 1):
    # Use the xpath to select the "short answer" fields in  Google Form.
    address_field = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field = driver.find_element(by=By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field = driver.find_element(by=By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    send_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    time.sleep(3)
    address_field.click()
    address_field.send_keys(addresses_list[i])
    price_field.click()
    price_field.send_keys(prices_list[i])
    link_field.click()
    link_field.send_keys(links_list[i])
    send_button.click()
    time.sleep(1)
    another_answer = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
