"""
Module to acquire Ubisoft ID from Ubisoft username using stats.cc
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re


def get_ubisoft_id_from_username(username: str) -> tuple[str | None, bool]:
    """
    Acquires Ubisoft ID from Ubisoft username by navigating to stats.cc/siege
    and extracting the ID from the resulting URL.
    
    Args:
        username: The Ubisoft username to search for
        
    Returns:
        tuple: (extracted_id, success) where success indicates if ID was found
    """
    driver = None
    try:
        # Initialize Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        
        driver.get("https://stats.cc/siege")
        
        # Wait for page to load and find search box
        wait = WebDriverWait(driver, 15)
        
        # Try multiple selectors for robustness
        search_box = None
        selectors = [
            (By.XPATH, "//input[@placeholder='Search a profile...']"),
            (By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[2]/main/div/div/div[1]/div[2]/input"),
            (By.CSS_SELECTOR, "input[placeholder='Search a profile...']"),
        ]
        
        for selector_type, selector_value in selectors:
            try:
                search_box = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                break
            except TimeoutException:
                continue
        
        if not search_box:
            return None, False
        
        # Scroll to search box to ensure it's visible
        driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
        time.sleep(0.5)
        
        # Enter username
        search_box.clear()
        search_box.click()
        time.sleep(0.3)
        search_box.send_keys(username)
        
        # Wait for autocomplete suggestions
        time.sleep(2)
        
        # Look for autocomplete suggestions/links
        url_pattern = r'https://stats\.cc/siege/[^/]+/[a-f0-9-]+'
        target_url = None
        
        try:
            suggestion_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/siege/']")
            if suggestion_links:
                # Find link that matches our username pattern
                for link in suggestion_links:
                    href = link.get_attribute('href')
                    if href and re.match(url_pattern, href) and username.lower() in href.lower():
                        target_url = href
                        break
                
                # If no exact match found, try first link
                if not target_url and suggestion_links:
                    href = suggestion_links[0].get_attribute('href')
                    if href and re.match(url_pattern, href):
                        target_url = href
                
                # Navigate directly to the URL
                if target_url:
                    driver.get(target_url)
                else:
                    # Try JavaScript click as fallback
                    driver.execute_script("arguments[0].click();", suggestion_links[0])
            else:
                # If no suggestions found, try pressing Enter
                search_box.send_keys(Keys.RETURN)
        except Exception:
            search_box.send_keys(Keys.RETURN)
        
        # Wait for navigation
        if target_url:
            time.sleep(2)
        else:
            try:
                wait.until(lambda d: re.match(url_pattern, d.current_url) is not None)
                time.sleep(1)
            except TimeoutException:
                pass
        
        current_url = driver.current_url
        
        # Extract Ubisoft ID from URL
        url_pattern = r'https://stats\.cc/siege/[^/]+/([a-f0-9-]+)'
        match = re.search(url_pattern, current_url)
        
        if match:
            extracted_id = match.group(1)
            return extracted_id, True
        else:
            return None, False
            
    except Exception:
        return None, False
    finally:
        if driver:
            driver.quit()

