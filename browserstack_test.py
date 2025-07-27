import traceback
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.webdriver import Options as SafariOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

print("✅ BrowserStack test script started", flush=True)

BROWSERSTACK_USERNAME = "prachisingh_WrTAvo"
BROWSERSTACK_ACCESS_KEY = "C46LBQpENkdPsTSqTiKA"

URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

CAPABILITIES = [
    {
        'os': 'Windows', 'os_version': '11', 'browser': 'Chrome', 'browser_version': 'latest', 'name': 'Win-Chrome'
    },
    {
        'os': 'OS X', 'os_version': 'Monterey', 'browser': 'Safari', 'browser_version': 'latest', 'name': 'Mac-Safari'
    },
    {
        'os': 'Windows', 'os_version': '10', 'browser': 'Firefox', 'browser_version': 'latest', 'name': 'Win-Firefox'
    },
    {
        'device': 'Samsung Galaxy S22',
        'real_mobile': 'true',
        'os_version': '12.0',
        'browserName': 'Chrome',
        'name': 'GalaxyS22'
    },
    {
        'device': 'iPhone 14',
        'real_mobile': 'true',
        'os_version': '16',
        'browserName': 'Safari',
        'name': 'iPhone14'
    },
]

def run_test(cap):
    print(f"🚀 Starting test on {cap['name']}", flush=True)
    driver = None
    try:
        browser = cap.get('browser') or cap.get('browserName')

        if browser == 'Chrome':
            options = ChromeOptions()
        elif browser == 'Firefox':
            options = FirefoxOptions()
        elif browser == 'Safari':
            options = SafariOptions()
        else:
            options = ChromeOptions()

        for key, value in cap.items():
            options.set_capability(key, value)

        options.set_capability('browserstack.user', BROWSERSTACK_USERNAME)
        options.set_capability('browserstack.key', BROWSERSTACK_ACCESS_KEY)
        options.set_capability('build', 'ElPais-Scraper')

        driver = webdriver.Remote(command_executor=URL, options=options)

        driver.get("https://elpais.com/")
        print(f"[{cap['name']}] Page loaded, title: '{driver.title}'", flush=True)

        # Wait for possible cookie consent popup and accept it if present
        time.sleep(3)  # wait for popup to appear (adjust if needed)
        try:
            consent_button = driver.find_element(By.CSS_SELECTOR, "button[class*='accept']")
            consent_button.click()
            print(f"[{cap['name']}] Cookie consent accepted.", flush=True)
        except Exception:
            print(f"[{cap['name']}] No cookie consent popup found.", flush=True)

        # Wait for main page content - example: header element present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "header"))
        )
        print(f"[{cap['name']}] Page ready, final title: '{driver.title}'", flush=True)

        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Page loaded and verified"}}'
        )

        driver.save_screenshot(f"{cap['name']}_screenshot.png")
        print(f"✅ Test passed on: {cap['name']}", flush=True)

    except Exception as e:
        print(f"❌ Test failed on {cap['name']}: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
        if driver:
            try:
                driver.execute_script(
                    'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "Test failed with exception"}}'
                )
            except:
                pass
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_test, CAPABILITIES)