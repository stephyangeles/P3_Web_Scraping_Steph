import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Directory where the generated images will be stored
IMAGE_DIR = os.path.join("src", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)  # Create the directory if it doesn't exist

def generate_color_image(hex_code, image_path, size=(200, 200)):
    # Remove '#' if present in the HEX code
    if hex_code.startswith('#'):
        hex_code_clean = hex_code[1:]
    else:
        hex_code_clean = hex_code
    try:
        # Convert HEX to RGB values
        r = int(hex_code_clean[0:2], 16)
        g = int(hex_code_clean[2:4], 16)
        b = int(hex_code_clean[4:6], 16)
    except Exception as e:
        print(f"Error converting HEX to RGB: {e}")
        r, g, b = 0, 0, 0
    # Create a new image with the specified color
    img = Image.new('RGB', size, (r, g, b))
    img.save(image_path)
    print(f"Generated image for {hex_code} at {image_path}")

def scrape_colors():
    
    # Configure Selenium to run in headless mode
    options = Options()
    options.add_argument('--headless')         # Run browser in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Target URL
    url = "https://htmlcolorcodes.com/color-names/"
    driver.get(url)
    print(f"Accessing {url} ...")

    # Attempt to close the cookies popup, if it appears
    try:
        accept_cookies = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        accept_cookies.click()
        print("Cookies popup closed.")
        time.sleep(2)  # Wait for the popup to disappear
    except Exception:
        print("No cookies popup found or it was already closed.")

    colors = []

    try:
        # Locate all rows from the color table
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody.color-table__body tr.color-table__row")
        print(f"Found {len(rows)} rows in the color table.")

        for row in rows:
            try:
                # Extract name, HEX code, and RGB code from each row
                name = row.find_element(By.CSS_SELECTOR, ".color-table__cell--name").text.strip()
                hex_code = row.find_element(By.CSS_SELECTOR, ".color-table__cell--hex").text.strip()
                rgb_code = row.find_element(By.CSS_SELECTOR, ".color-table__cell--rgb").text.strip()

                # Generate an image based on the HEX code
                img_filename = os.path.join(IMAGE_DIR, f"{hex_code}.png")
                generate_color_image(hex_code, img_filename)

                # Append the extracted data to the list
                colors.append({
                    "name": name,
                    "hex": hex_code,
                    "rgb": rgb_code,
                    "image": img_filename
                })

            except Exception as e:
                print(f"Error extracting data from a row: {e}")

    except Exception as e:
        print(f"Error loading the color table: {e}")

    # Close the browser session
    driver.quit()
    print("Browser closed.")
    return colors

# Test the function by executing it if the script is run directly
if __name__ == "__main__":
    color_data = scrape_colors()
    print("Scraped Colors:")
    # Print only the first 5 colors for verification
    for color in color_data[:5]:
        print(color)
