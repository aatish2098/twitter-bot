import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_tweet_metrics(tweet_id: int):
    # Set up Selenium WebDriver with Chrome
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver_path = "./chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the tweet URL
        url = f"https://x.com/i/web/status/{tweet_id}"
        driver.get(url)

        # Wait for the article to load
        article = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )

        # Initialize the metrics
        metrics = {"replies": "0", "reposts": "0", "likes": "0", "bookmarks": "0", "views": "0"}

        # Fetch metrics using aria-labels
        for key, label in {
            "replies": "Reply",
            "reposts": "Repost",
            "likes": "Like",
            "bookmarks": "Bookmark",
        }.items():
            try:
                element = article.find_element(By.XPATH, f".//button[contains(@aria-label, '{label}')]")
                metrics[key] = element.get_attribute("aria-label").split(" ")[0]
            except Exception:
                metrics[key] = "0"  # Default to 0 if not found

        # Fetch views (different location, may not be in a button)
        try:
            views_element = article.find_element(By.XPATH, ".//div[contains(@aria-label, 'views')]")
            metrics["views"] = views_element.get_attribute("aria-label").split(" ")[0]
        except Exception:
            metrics["views"] = "0"  # Default to 0 if not found

        return metrics
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()

def fetch_tweet_content(tweet_id: int):
    # Set up Selenium WebDriver with Chrome
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Path to your ChromeDriver
    driver_path = "./chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to the tweet URL
        url = f"https://x.com/i/web/status/{tweet_id}"
        driver.get(url)

        # Wait for the page to load (adjust the sleep time if needed)
        time.sleep(4)

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

