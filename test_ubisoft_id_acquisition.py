"""
Test script for acquiring Ubisoft ID from Ubisoft username.
Tests the logic described in PLAN.MD section "ACQUIRING UBISOFT ID FROM UBISOFT USERNAME"
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re


def get_ubisoft_id_from_username(username: str, expected_id: str = None) -> tuple[str, bool]:
    """
    Acquires Ubisoft ID from Ubisoft username by navigating to stats.cc/siege
    and extracting the ID from the resulting URL.
    
    Args:
        username: The Ubisoft username to search for
        expected_id: Optional expected ID for validation
        
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
        
        print(f"Navigating to https://stats.cc/siege...")
        driver.get("https://stats.cc/siege")
        
        # Wait for page to load and find search box using placeholder text (more reliable)
        wait = WebDriverWait(driver, 15)
        print("Waiting for search box to load...")
        
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
                print(f"✓ Found search box using {selector_type}")
                break
            except TimeoutException:
                continue
        
        if not search_box:
            raise NoSuchElementException("Could not find search box with any selector")
        
        # Scroll to search box to ensure it's visible
        driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
        time.sleep(0.5)
        
        print(f"Entering username '{username}' into search box...")
        search_box.clear()
        search_box.click()  # Ensure focus
        time.sleep(0.3)
        search_box.send_keys(username)
        
        # Wait for autocomplete suggestions to appear (they appear as links)
        print("Waiting for autocomplete suggestions...")
        time.sleep(2)
        
        # Look for autocomplete suggestions/links that match the username
        url_pattern = r'https://stats\.cc/siege/[^/]+/[a-f0-9-]+'
        initial_url = driver.current_url
        
        # Try to find and navigate to the suggestion link
        target_url = None
        try:
            # Look for links in autocomplete dropdown
            suggestion_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/siege/']")
            if suggestion_links:
                # Find link that matches our username pattern
                for link in suggestion_links:
                    href = link.get_attribute('href')
                    if href and re.match(url_pattern, href) and username.lower() in href.lower():
                        print(f"Found matching suggestion link: {href}")
                        target_url = href
                        break
                
                # If no exact match found, try first link
                if not target_url and suggestion_links:
                    href = suggestion_links[0].get_attribute('href')
                    if href and re.match(url_pattern, href):
                        print(f"Using first suggestion link: {href}")
                        target_url = href
                
                # Navigate directly to the URL (bypasses overlay issues)
                if target_url:
                    print(f"Navigating directly to: {target_url}")
                    driver.get(target_url)
                else:
                    # If no valid URL found, try clicking with JavaScript
                    print("Attempting JavaScript click on first suggestion...")
                    driver.execute_script("arguments[0].click();", suggestion_links[0])
            else:
                # If no suggestions found, try pressing Enter
                print("No suggestions found, pressing Enter...")
                search_box.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Error finding suggestion: {e}, trying Enter key...")
            search_box.send_keys(Keys.RETURN)
        
        # Wait for navigation to the profile page
        # Expected URL format: https://stats.cc/siege/[UBISOFT_USERNAME]/[UBISOFT_ID]
        print("Waiting for page to load...")
        
        if target_url:
            # If we navigated directly, wait for page load
            time.sleep(2)  # Give page time to load
            print("✓ Direct navigation successful!")
        else:
            # If we used Enter key or click, wait for URL to change
            try:
                # Wait up to 15 seconds for URL to change to expected pattern
                wait.until(lambda d: re.match(url_pattern, d.current_url) is not None)
                time.sleep(1)  # Brief wait to ensure page fully loaded
                print("✓ Navigation successful!")
            except TimeoutException:
                print(f"Timeout waiting for navigation. Current URL: {driver.current_url}")
                # Check if URL changed at all
                if driver.current_url != initial_url:
                    print(f"URL changed but doesn't match expected pattern")
                else:
                    print("URL did not change")
        
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        # Extract Ubisoft ID from URL
        # Pattern: https://stats.cc/siege/[username]/[id]
        url_pattern = r'https://stats\.cc/siege/[^/]+/([a-f0-9-]+)'
        match = re.search(url_pattern, current_url)
        
        if match:
            extracted_id = match.group(1)
            print(f"✓ Successfully extracted Ubisoft ID: {extracted_id}")
            
            # Validate against expected ID if provided
            if expected_id:
                if extracted_id.lower() == expected_id.lower():
                    print(f"✓ Extracted ID matches expected ID!")
                    return extracted_id, True
                else:
                    print(f"✗ Mismatch! Expected: {expected_id}, Got: {extracted_id}")
                    return extracted_id, False
            
            return extracted_id, True
        else:
            print(f"✗ Could not extract Ubisoft ID from URL: {current_url}")
            return None, False
            
    except TimeoutException:
        print("✗ Timeout: Could not find search box or page did not load in time")
        return None, False
    except NoSuchElementException as e:
        print(f"✗ Element not found: {e}")
        return None, False
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        return None, False
    finally:
        if driver:
            driver.quit()


def test_ubisoft_id_acquisition():
    """Main test function"""
    print("=" * 60)
    print("Testing Ubisoft ID Acquisition Logic")
    print("=" * 60)
    print()
    
    test_username = "sauni."
    expected_id = "934e0849-2c26-4067-a66a-7636c152d0e5"
    
    print(f"Test Username: {test_username}")
    print(f"Expected ID: {expected_id}")
    print()
    
    extracted_id, success = get_ubisoft_id_from_username(test_username, expected_id)
    
    print()
    print("=" * 60)
    if success and extracted_id:
        print("TEST RESULT: ✓ PASSED")
    else:
        print("TEST RESULT: ✗ FAILED")
    print("=" * 60)
    
    return success


if __name__ == "__main__":
    test_ubisoft_id_acquisition()

