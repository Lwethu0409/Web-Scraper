import requests
import boto3
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin

# 1. Website URL
url = "https://quotes.toscrape.com/"

# 2. Connect to DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)

table = dynamodb.Table("QuotesTable")

# 3. Start scraping
quote_id = 0
total_quotes = 0

while url:

    print("\nScraping:", url)

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    print("Quotes found:", len(quotes))

    # 4. Extract each quote
    for quote in quotes:

        quote_id += 1

        quote_text = quote.find(
            "span", class_="text"
        ).get_text(strip=True)

        author_name = quote.find(
            "small", class_="author"
        ).get_text(strip=True)

        tags = quote.find_all("a", class_="tag")

        tag_list = [
            tag.get_text(strip=True) for tag in tags
        ]

        scraped_at = datetime.now(timezone.utc).isoformat()

        # 5. Save to DynamoDB
        table.put_item(
            Item={
                "Quote_Id": str(quote_id),
                "Author_Name": author_name,
                "Quote_Text": quote_text,
                "Tags": tag_list,
                "Scraped_At": scraped_at
            }
        )

        total_quotes += 1

        print("Saved quote:", quote_id, "|", author_name)

    # 6. Find the next page
    next_button = soup.find("li", class_="next")

    if next_button:
        next_link = next_button.find("a")["href"]
        url = urljoin(url, next_link)
    else:
        url = None

# 7. Finish
print("\n--------------------------------")
print("SCRAPING COMPLETED!")
print("Total quotes saved:", total_quotes)
print("--------------------------------")