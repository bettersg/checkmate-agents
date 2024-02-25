from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import json
import os
import re

# Setup Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Selenium Grid URL running in Docker
webdriver_host = os.getenv('WEBDRIVER_HOST')

print(webdriver_host)

# Set desired capabilities
desired_capabilities = DesiredCapabilities.CHROME.copy()

# Connect to Selenium
driver = webdriver.Remote(command_executor=webdriver_host,
                          options=chrome_options)

# Tool 2
def get_page_text(link):
  driver.get(link)
  page_source = driver.page_source
  soup = BeautifulSoup(page_source, 'html.parser')
  raw_text = soup.get_text()
  cleaned_newline_text = re.sub(r'\n+', '\n', raw_text) #reduce tokens
  cleaned_text = re.sub(r'\s+', ' ', cleaned_newline_text) #reduce tokens
  return cleaned_text