from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options
import csv
from selenium.common.exceptions import TimeoutException, WebDriverException
import sys

# driver initialization
driver = webdriver.Chrome(options=Options())

driver.get("https://www.thepwhl.com/en/stats/player-stats/all-teams/1?sort=points&playertype=skater&position=skaters&rookie=no&statstype=standard&page=1&league=1")

# explicit wait statement
element = WebDriverWait(driver, 10).until( 
        EC.visibility_of_element_located((By.CLASS_NAME, "ht-odd-row"))
        )

wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d : element.is_displayed())

def ParseFunction(html):
    csvwriter = csv.writer(c)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs={'class':'ht-table'})
    try:
      table_body = table.find('tbody')
    except AttributeError:
      print("Attribute Error")
      return 1
    rows = table_body.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      if (len(cols) >= 2): 
        if (len(cols[0]) >= 1):
          cols.pop(1)
          cols.pop(1)
          if (cols[1][len(cols[1]) - 1] == '-'):
            cols[1] = cols[1][:-3]
          csvwriter.writerow([ele for ele in cols if ele]) # Get rid of empty values

url = "https://www.thepwhl.com/en/stats/player-stats/all-teams/1?sort=points&playertype=skater&position=skaters&rookie=no&statstype=standard&page=1&league=1"

pg_number = 2
sentinel = True
with open(r"C:\Users\cashm\Downloads\pwhl-fantasy\PlayerOutput.csv", 'w+', encoding='utf16') as c:
  while sentinel:
    sentinel2 = True
    while sentinel2:
      # html file inialization
      html = driver.page_source
      resp = ParseFunction(html)
      if (resp == 1):
        #print(driver.current_url)
        #print("resp = 1")
        sentinel2 = True
      else:
        #print(driver.current_url)
        #print("resp =/= 1")
        sentinel2 = False
    try:
      url = "https://www.thepwhl.com/en/stats/player-stats/all-teams/1?sort=points&playertype=skater&position=skaters&rookie=no&statstype=standard&page=" + str(pg_number) + "&league=1"
      driver.get(url)
    except (TimeoutException, WebDriverException) as e:
       print("Time out or Web Driver exception")
    pg_number += 1
    if (pg_number >= 9):
      driver.quit()
      sentinel = False
      break

# exit statement for task scheduler
sys.exit(0)