from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from bs4 import BeautifulSoup
from constants import UserNotFoundException, ExitCode

# Webdriver options
chrome_options = webdriver.ChromeOptions()
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"


def scrape(username, show_window=False, load_images=False, debug=False):
    if debug:
        show_window = True
        load_images = True

    if not show_window:
        # Go headless
        chrome_options.add_argument("--headless=new")

    if not load_images:
        # Disable images for faster website load
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"https://krunker.io/social.html?p=profile&q={username}")
        if debug:
            input("Press [Enter] to continue.")
        else:
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
        exit(ExitCode.SELENIUM_TIMEOUT)

    # Ignore "Name "driver" can be undefined" - Program exits if Selenium fucks up anyway
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')
    if soup.find(text="Profile doesn't exist"):
        print(f"Krunker profile '{username}' was not found!")
        exit(ExitCode.USERNAME_NOT_FOUND)

    try:
        meta_div = soup.body.find("div", {"class": "leftTopHolder"})
        xp_div = soup.body.find("div", {"class": "xpBar"})
        main_stat_divs = soup.body.find_all("div", {"class": "pSt"})
        class_xp_divs = soup.body.find_all("div", {"class": "classCard"})

        driver.quit()

        return {
            "meta": meta_div.get_text(),
            "xpbar": xp_div.get_text(),
            "main_stats": [div.get_text() for div in main_stat_divs],
            "class_stats": [div.get_text() for div in class_xp_divs]
        }
    except AttributeError:
        print("The HTML could not be parsed.\n"
              "Most likely, there is a captcha. Please solve it manually, and try again.\n"
              "You can do this by adding the `headless=False` flag in the args of `krunker_api`.")
        exit(ExitCode.COULDNT_LOAD_HTML)
