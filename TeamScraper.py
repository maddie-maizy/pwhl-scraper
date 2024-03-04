from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
import csv
import sys

# driver initialization
driver = webdriver.Chrome()

driver.get("https://www.thepwhl.com/en/home-page-stats")

# explicit wait statement
element = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.CLASS_NAME, "table-container")) 
    ) 

wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d : element.is_displayed())



with open(r"C:\Users\cashm\Downloads\pwhl-fantasy\TeamOutput.csv", 'w+') as c:
    sentinel = True
    while sentinel:
      # html file inialization
      html = driver.page_source
      csvwriter = csv.writer(c)
      temp_array = []
      soup = BeautifulSoup(html, 'html.parser')
      table = soup.find('table', attrs={'class':'ht-table'})
      sentinel = False
      try:
        table_body = table.find('tbody')
      except AttributeError:
        print("Attribute Error")
        sentinel = True
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        csvwriter.writerow([ele for ele in cols if ele]) # Get rid of empty values

# exit statement for task scheduler
sys.exit(0)