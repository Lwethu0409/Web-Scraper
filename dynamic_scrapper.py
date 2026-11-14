import boto3
from datetime import datetime, timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 1. Connect to DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)

table = dynamodb.Table("MoviesTable")


# 2. Open Chrome
driver = webdriver.Chrome()

try:

    # 3. Open the dynamic website
    driver.get(
        "https://www.scrapethissite.com/pages/ajax-javascript/"
    )

    wait = WebDriverWait(driver, 20)

    # 4. Select 2015 to trigger JavaScript/AJAX loading
    year_button = wait.until(
        EC.element_to_be_clickable((By.ID, "2015"))
    )

    year_button.click()

    print("Selected year: 2015")
    print("Waiting for movie data...")

    # 5. Wait for movie records to appear
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "tr.film")
        )
    )

    rows = driver.find_elements(
        By.CSS_SELECTOR, "tr.film"
    )

    print("Movies found:", len(rows))
    print("--------------------------------")

    movies_data = []

    # 6. Extract movie information
    for index, row in enumerate(rows, start=1):

        movie = {
            "Movie_Id": str(index),

            "Movie_Title": row.find_element(
                By.CSS_SELECTOR, ".film-title"
            ).text.strip(),

            "Year": "2015",

            "Nominations": row.find_element(
                By.CSS_SELECTOR, ".film-nominations"
            ).text.strip(),

            "Awards": row.find_element(
                By.CSS_SELECTOR, ".film-awards"
            ).text.strip(),

            "Scraped_At": datetime.now(
                timezone.utc
            ).isoformat()
        }

        movies_data.append(movie)

    print("Total movies extracted:", len(movies_data))
    print("--------------------------------")

    # 7. Save movies to DynamoDB
    for movie in movies_data:

        table.put_item(
            Item=movie
        )

        print("Movie:", movie["Movie_Title"])
        print("Saved to DynamoDB!")
        print("--------------------------------")

    print("SCRAPING COMPLETED SUCCESSFULLY!")
    print("Total movies saved:", len(movies_data))


except Exception as error:

    print("An error occurred:", error)


finally:

    # 8. Close Chrome
    driver.quit()
    print("Browser closed.")