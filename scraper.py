from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from bs4 import BeautifulSoup
from constants import UserNotFoundException

# Webdriver options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}  # Disable images for faster loads
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless=new")
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"


def scrape(username):
    try:
        #       execute chrome webdriver
        #   * chromedriver now works for me *
        #       !!chrome number one!!
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"https://krunker.io/social.html?p=profile&q={username}")

        # wait for website loading
        # Accept privacy policy
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )

        # Once the button is clickable, click it
        button.click()
        logging.info('website loaded successfully!')
    except TimeoutException:
        print("Browser driver has timed out. Please try again.")
        exit(1)

    # Ignore "Name "driver" can be undefined" - Program exits if Selenium fucks up anyway
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')
    if soup.find(text="Profile doesn't exist"):
        raise UserNotFoundException(f"Krunker profile '{username}' was not found!")

    meta_div = soup.body.find("div", {"class": "leftTopHolder"})
    xp_div = soup.body.find("div", {"class": "xpBar"})
    main_stat_divs = soup.body.find_all("div", {"class": "pSt"})
    class_xp_divs = soup.body.find_all("div", {"class": "classCard"})

    # Quit headless browser
    driver.quit()

    return {
        "meta": meta_div.get_text(),
        "xpbar": xp_div.get_text(),
        "main_stats": [div.get_text() for div in main_stat_divs],
        "class_stats": [div.get_text() for div in class_xp_divs]
    }
