# 📦 Import the tools we need
import requests  # to go to the website
from bs4 import BeautifulSoup  # to read and extract info from the website
import pandas as pd  # to save the data into a CSV file
import schedule  # to run the scraper automatically
import time
import logging  # to write logs
from datetime import datetime

# 📝 Set up logging (this will create a log file to track what happens)
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# 🧠 Step 1: Scrape the website and get the top 10 job posts
def scrape_jobs():
    try:
        logging.info("Starting the scraping process...")
        base_url = "https://vacancymail.co.zw"
        url = f"{base_url}/jobs/"
        response = requests.get(url)
        response.raise_for_status()

        # 🧹 Step 2: Clean and read the website content
        soup = BeautifulSoup(response.content, "html.parser")
        job_cards = soup.find_all(
            "a", class_="job-listing")  # Correct selector

        jobs = []

        for card in job_cards[:10]:  # Take only top 10
            try:
                title = card.find(
                    "h3", class_="job-listing-title").get_text(strip=True)
                company = card.find(
                    "h4", class_="job-listing-company").get_text(strip=True)
                description = card.find(
                    "p", class_="job-listing-text").get_text(strip=True)

                # Footer info (location, expiry, etc.)
                footer_items = card.find(
                    "div", class_="job-listing-footer").find_all("li")
                location = expiry = "N/A"
                for item in footer_items:
                    text = item.get_text(strip=True)
                    if "Expires" in text:
                        expiry = text
                    elif any(city in text for city in ["Harare", "Bulawayo", "Mutare"]):
                        location = text

                # Optional: Job detail link
                link = base_url + card.get("href", "")

                jobs.append({
                    "Job Title": title,
                    "Company": company,
                    "Location": location,
                    "Expiry Date": expiry,
                    "Description": description,
                    "Job Link": link
                })

            except Exception as e:
                logging.warning(f"Skipped a card due to error: {e}")
                continue

        if not jobs:
            print("⚠️ No jobs found.")
            return

        # 🗃️ Step 3: Put the data in a table (DataFrame)
        df = pd.DataFrame(jobs)
        df.drop_duplicates(inplace=True)

        # 🔽 Step 4: Save the data into CSV
        filename = f"scraped_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        df.to_csv(filename, index=False)

        logging.info(
            f"✅ Successfully scraped and saved {len(df)} job posts to {filename}")
        print(f"✅ Scraped {len(df)} jobs and saved to {filename}")

    except Exception as e:
        logging.error(f"❌ Error during scraping: {e}")
        print(f"❌ Error: {e}")


# 🔁 Step 2 (Optional): Schedule the scraping daily at 8:00 AM
def schedule_scraping():
    schedule.every().day.at("08:00").do(scrape_jobs)

    print("📅 Scheduled job scraping. Waiting to run every day at 8:00 AM.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


# 🚀 Step 3: Run the script
if __name__ == "__main__":
    # Run once now:
    scrape_jobs()

    # Or uncomment to run daily:
    # schedule_scraping()
