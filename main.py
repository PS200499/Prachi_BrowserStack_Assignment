import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
from urllib.request import urlretrieve
from deep_translator import GoogleTranslator
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_articles():
    os.makedirs("images", exist_ok=True)
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    driver.get("https://elpais.com/")
    time.sleep(3)

    try:
        opinion_link = driver.find_element(By.LINK_TEXT, "Opinión")
        opinion_url = opinion_link.get_attribute("href")
        driver.get(opinion_url)
        time.sleep(3)
    except Exception as e:
        print("❌ Could not navigate to Opinión section:", e)
        driver.quit()
        return []

    articles_data = []

    for i in range(5):
        articles = driver.find_elements(By.CSS_SELECTOR, "article")
        if i >= len(articles):
            print(f"⚠️ Only found {len(articles)} articles.")
            break

        try:
            article = articles[i]
            header = article.find_element(By.CSS_SELECTOR, "h2 a")
            title = header.text.strip()
            if not title:
                title = header.get_attribute("title") or header.get_attribute("aria-label")
            if not title or title.strip() == "":
                try:
                    title = header.get_attribute("href").strip("/").split("/")[-1].replace("-", " ").capitalize()
                except:
                    title = "untitled"
            if not title:
                title = header.get_attribute("title") or header.get_attribute("aria-label") or "untitled"
            safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title[:50])
            url = header.get_attribute("href")

            driver.get(url)
            time.sleep(2)

            paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.a_st > p")
            content = "\n".join([p.text for p in paragraphs if p.text.strip()])

            try:
                img = driver.find_element(By.CSS_SELECTOR, "figure img")
                img_url = img.get_attribute("src")
                img_name = safe_title + ".jpg"
                img_path = os.path.join("images", img_name)
                urlretrieve(img_url, os.path.join(os.getcwd(), img_path))
            except Exception as img_error:
                print(f"⚠️ No image found for: {title} — {img_error}")
                img_path = "No image"

            articles_data.append({
                "title": title,
                "content": content,
                "image": img_path
            })

        except Exception as e:
            print("❌ Error fetching article:", e)

        driver.back()
        time.sleep(2)

    driver.quit()
    return articles_data

def translate_titles(titles):
    translated = [GoogleTranslator(source='es', target='en').translate(title) for title in titles]
    return translated

def analyze_words(translated_titles):
    from collections import Counter
    all_words = " ".join(translated_titles).lower().split()
    counter = Counter(all_words)
    repeated = {word: count for word, count in counter.items() if count > 2}
    return repeated

if __name__ == "__main__":
    articles = scrape_articles()
    print("\n--- Articles in Spanish ---\n")
    for art in articles:
        print(f"Title: {art['title']}\nContent: {art['content'][:200]}...\nImage: {art['image']}\n")

    translated = translate_titles([a["title"] for a in articles])
    print("\n--- Translated Titles ---\n")
    for title in translated:
        print(title)

    repeated_words = analyze_words(translated)
    print("\n--- Repeated Words in Translated Titles ---\n")
    for word, count in repeated_words.items():
        print(f"{word}: {count}")
