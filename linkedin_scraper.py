from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
from config import KEYWORDS, DAYS_BACK
from utils import is_recent, contains_free_terms, extract_links
from datetime import datetime

load_dotenv()

def linkedin_login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(os.getenv("LINKEDIN_EMAIL"))     
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(os.getenv("LINKEDIN_PASSWORD")) 
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(5)  

def scrape_linkedin():
    driver = webdriver.Chrome()
    linkedin_login(driver)
    results = []

    for keyword in KEYWORDS:
        driver.get(f"https://www.linkedin.com/search/results/content/?keywords={keyword}")
        time.sleep(5)
        posts = driver.find_elements(By.CLASS_NAME, "update-components-text")  

        for post in posts:
            text = post.text
            post_date = datetime.now() 
            if is_recent(post_date, DAYS_BACK) and contains_free_terms(text):
                results.append({
                    "platform": "LinkedIn",
                    "keyword": keyword,
                    "text": text,
                    "date": post_date,
                    "links": extract_links(text)
                })

    driver.quit()
    return results
