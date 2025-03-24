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
from scraper.models import Color, Palette, PaletteColor

# Directory where the generated images will be stored
IMAGE_DIR = os.path.join("src", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)  # Create the directory if it doesn't exist

def generate_color_image(hex_code, image_path, size=(200, 200)):
    """Generate an image with the specified color."""
    if hex_code.startswith('#'):
        hex_code_clean = hex_code[1:]
    else:
        hex_code_clean = hex_code
    try:
        r = int(hex_code_clean[0:2], 16)
        g = int(hex_code_clean[2:4], 16)
        b = int(hex_code_clean[4:6], 16)
    except Exception as e:
        print(f"Error converting HEX to RGB: {e}")
        r, g, b = 0, 0, 0
    img = Image.new('RGB', size, (r, g, b))
    img.save(image_path)
    print(f"Generated image for {hex_code} at {image_path}")

def scrape_colors():
    
    options = Options()
    options.add_argument('--headless')         
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    url = "https://htmlcolorcodes.com/colors/"
    driver.get(url)
    print(f"Accessing {url} ...")
    
    try:
        accept_cookies = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        accept_cookies.click()
        print("Cookies popup closed.")
        time.sleep(2)
    except Exception:
        print("No cookies popup found or it was already closed.")
    
    colors = []
    try:
        color_elements = driver.find_elements(By.CSS_SELECTOR, "div.color-table__color.js-color")
        print(f"Found {len(color_elements)} color elements.")

        for color_div in color_elements:
            try:
                hex_code = color_div.get_attribute("data-hex")
                rgb_code = color_div.get_attribute("data-rgb")
                
                name = color_div.find_element(By.XPATH, "./ancestor::td/following-sibling::td[@class='color-table__cell--name']").text.strip()
                
                img_filename = os.path.join(IMAGE_DIR, f"{hex_code.replace('#', '')}.png")
                generate_color_image(hex_code, img_filename, size=(100, 100))
                
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
    
    driver.quit()
    print("Browser closed.")
    return colors


def scrape_palettes():
    options = Options()
    options.add_argument('--headless')         
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    url = "https://www.colorhunt.co/"
    driver.get(url)
    print(f"Accessing {url} ...")
    
    try:
        accept_cookies = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]")
        ))
        accept_cookies.click()
        print("Cookies popup closed.")
        time.sleep(2)
    except Exception:
        print("No cookies popup found or it was already closed.")
    
    palettes = []
    
    try:
        palette_elements = driver.find_elements(By.CSS_SELECTOR, "div.item[data-code]")
        print(f"Found {len(palette_elements)} palettes.")

        for element in palette_elements:
            try:
                palette_code = element.get_attribute("data-code")
                palette_container = element.find_element(By.CSS_SELECTOR, "div.palette")
                color_elements = palette_container.find_elements(By.CSS_SELECTOR, "div.place")
    
                
                def rgba_to_hex(rgba):
                    rgba = rgba.replace("rgba(", "").replace("rgb(", "").replace(")", "")
                    r, g, b = map(int, rgba.split(",")[:3])
                    return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()
                
                hex_colors = [rgba_to_hex(color.value_of_css_property("background-color")) for color in color_elements]
                
                palettes.append({
                    "code": palette_code,
                    "colors": hex_colors
                })
            except Exception as e:
                print(f"Error extracting data from a palette: {e}")
    except Exception as e:
        print(f"Error obtaining palettes: {e}")
    
    driver.quit()
    print("Browser closed.")
    return palettes

def generate_palette_image(hex_colors, image_path, size=(200, 50)):
   
    from PIL import Image, ImageDraw
    width, height = size
    num_colors = len(hex_colors)
    stripe_width = width // num_colors
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for i, hex_color in enumerate(hex_colors):
        
        hex_clean = hex_color.lstrip('#')
        try:
            r = int(hex_clean[0:2], 16)
            g = int(hex_clean[2:4], 16)
            b = int(hex_clean[4:6], 16)
        except Exception as e:
            print(f"Error converting {hex_color} to RGB: {e}")
            r, g, b = 0, 0, 0
        x0 = i * stripe_width
        x1 = (i + 1) * stripe_width if i < num_colors - 1 else width
        draw.rectangle([x0, 0, x1, height], fill=(r, g, b))
    img.save(image_path)
    print(f"Generated palette image at {image_path}")


if __name__ == "__main__":
    color_data = scrape_colors()
    print("Scraped Colors:")
    for color in color_data[:25]:
        print(color)
    
    palette_data = scrape_palettes()
    print("Scraped Palettes:")
    for palette in palette_data[:5]:
        print(palette)

