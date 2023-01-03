from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv
import time

driver = webdriver.Chrome("C:\Program Files (x86)\ChromeDriver\chromedriver.exe")

driver.get("https://fantasy.espn.com/football/players/projections")
driver.maximize_window()
data = []
option = driver.find_elements(By.XPATH, "//select")
drop = Select(option[2])
drop.select_by_visible_text("2022 Season")
for i in range(8):
    content = driver.find_elements(By.XPATH, "//span/a")
    projected = driver.find_elements(By.XPATH, "//td/div[@title='Fantasy Points']")
    team = driver.find_elements(By.XPATH, "//span[@class='player-teamname']")
    position = driver.find_elements(By.XPATH, "//span[@class='position-eligibility']")
    src = driver.find_elements(By.XPATH, "//div[contains(@class, 'Image__Wrapper aspect-ratio--child')]/img")
    photos = []
    for i in src:
        photos.append(i.get_attribute("src"))
    proj = 1
    for k, j in enumerate(content):
        if j.text == "Learn More" or j.text == "Shop Now" or j.text == "Try Now":
            pass
        else:
            if proj > 99:
                break;
            defensetest = j.text.strip().split(' ')
            if defensetest[1] == "D/ST":
                t, p = defensetest[0], "D/ST"
                team.insert(k, t)
                position.insert(k, p)
            else: 
                t, p = team[k].text, position[k].text
            data.append([j.text.strip(), t, p, projected[proj].text, photos[k]])
            proj += 2
    button = driver.find_element(By.XPATH, "//nav/button[2]")
    button.click()
    time.sleep(2)
    
    button = driver.find_element(By.XPATH, "//nav/button[2]")
    
header = ['Player Name', 'Team', 'Position', '2022 Projected Points', 'PhotoURL']

with open('players.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
driver.quit()