from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
AUTH = os.getenv("AUTH")
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    print("Connecting to Scraping Browser...")
    # retrieving html of page
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html

def extract_body_content(html_content):
    # parsing up the retrieved html
    soup = BeautifulSoup(html_content,"html.parser")
    # retreiving body tag content
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,"html.parser")

    for script_or_style in soup(["script","style"]):
        # removing script/style tag content
        script_or_style.extract()
    
    # removing unnecessary \n chars
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

# splitting content/text into batches so LLM can process it (without exceeding max limit)
# feed LLM one batch at a time
def split_dom_content(dom_content,max_length = 6000):
    batches = []

    for i in range(0,len(dom_content),max_length):
        batch = dom_content[ i : i + max_length ]
        batches.append(batch)
    
    return batches



