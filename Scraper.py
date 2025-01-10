from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def fetch_tweet_content(tweet_id):
    # Set up Selenium WebDriver with Chrome
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Path to your ChromeDriver
    driver_path = "C:\\Users\\user\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the tweet URL
        url = f"https://x.com/i/web/status/{tweet_id}"
        driver.get(url)

        # Wait for the page to load (adjust the sleep time if needed)
        time.sleep(2)

        # Extract the <title> tag content
        title = driver.title

        # Clean up the title to extract only the tweet content
        if "on X:" in title:
            tweet_text = title.split("on X:")[1].strip()
        else:
            tweet_text = title

        # Remove the trailing "/ X"
        tweet_text = tweet_text.replace(' / X', '').strip()

        return tweet_text
    except Exception as e:
        return f"Error fetching tweet content: {e}"
    finally:
        driver.quit()

if __name__ == "__main__":
    # Example usage with multiple tweet IDs
    tweet_ids = [
        "1877469236626395590",
        "1877575510366011552"
    ]

    for tweet_id in tweet_ids:
        tweet_content = fetch_tweet_content(tweet_id)
        print(f"Tweet ID: {tweet_id}\nContent: {tweet_content}\n")
