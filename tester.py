#!/usr/bin/env python3
"""
tester.py
Simple site tester: visits links and attempts to click buttons.
Usage examples:
  python3 tester.py --url https://example.com
  python3 tester.py --url https://example.com --headless
"""
import argparse
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait

def wait_for_page_load(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except Exception:
        pass

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", "-u", required=True, help="Starting URL to test")
    p.add_argument("--headless", action="store_true", help="Run browser headless")
    args = p.parse_args()

    options = webdriver.FirefoxOptions()
    if args.headless:
        options.headless = True

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_page_load_timeout(30)

    try:
        base = args.url
        print("Opening", base)
        driver.get(base)
        wait_for_page_load(driver)

        # Collect links
        anchors = driver.find_elements(By.TAG_NAME, "a")
        hrefs = []
        for a in anchors:
            href = a.get_attribute("href")
            if not href:
                continue
            if href.startswith("javascript:") or href.startswith("#"):
                continue
            href = urljoin(base, href)
            hrefs.append(href)
        # dedupe while preserving order
        hrefs = list(dict.fromkeys(hrefs))
        print(f"Found {len(hrefs)} links. Visiting each (may take a while)...")

        for i, href in enumerate(hrefs, 1):
            try:
                print(f"[{i}/{len(hrefs)}] Visiting: {href}")
                driver.get(href)
                wait_for_page_load(driver)
                print(" Title:", driver.title)
                time.sleep(1)
            except Exception as e:
                print(" Error visiting:", e)

        # Go back to base and test <button> elements
        print("Returning to base and testing buttons...")
        driver.get(base)
        wait_for_page_load(driver)
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(buttons)} <button> elements. Clicking each once (best-effort).")

        for idx, btn in enumerate(buttons, 1):
            try:
                txt = btn.text.strip() or btn.get_attribute("aria-label") or btn.get_attribute("id") or "<no-text>"
                print(f"[{idx}] Clicking button: {txt}")
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                btn.click()
                time.sleep(2)
                wait_for_page_load(driver)
                print(" Now page:", driver.title, "| URL:", driver.current_url)
                driver.back()
                wait_for_page_load(driver)
            except Exception as e:
                print(" Error clicking:", e)

        print("Finished run.")
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
