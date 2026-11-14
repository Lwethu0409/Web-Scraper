# Praesignis AWS re/Start - Web Scraping & DynamoDB Pipeline
A cloud-integrated web scraping project developed as part of the Praesignis AWS re/Start program. This repository contains two automated scraper implementations (static via BeautifulSoup and dynamic via Selenium) that extract web data and persist it into an AWS DynamoDB table.
## Project Architecture & Features
 * *Part 1: Static Scraping (requests + BeautifulSoup)*
   * Fetches raw HTML efficiently from static websites (e.g., [http://quotes.toscrape.com/](http://quotes.toscrape.com/)).
   * Parses elements to extract text, authors, and associated tags.
 * *Part 2: Dynamic Scraping (Selenium)*
   * Handles JavaScript-rendered web pages and dynamic content loading (e.g., [http://quotes.toscrape.com/js/](http://quotes.toscrape.com/js/)).
   * Automates browser actions and explicit wait times for elements to render.
 * *Cloud Persistence (AWS DynamoDB)*
   * Connects securely using boto3.
   * Stores structured items using composite primary keys (Quote_id as Partition Key and Author_name as Sort Key) alongside custom timestamps (Scraped_at).
## Repository Structure
text
├── scrapper.py        # Part 1: Static scraper using Requests and BeautifulSoup
├── dynamic_scrapper.py       # Part 2: Dynamic browser scraper using Selenium
└── README.md                 # Project documentation


## ⚙️ Setup and Installation
### 1. Prerequisites
 * Python 3.8+ installed on your machine.
 * An active AWS Account with an IAM user configured with programmatic access and AmazonDynamoDBFullAccess permissions.
 * Browser WebDriver installed (ChromeDriver for Chrome or msedgedriver for Edge) matching your browser version.
### 2. Configure AWS CLI
Open your terminal and configure your AWS credentials and region:
bash
aws configure


 * Provide your *AWS Access Key ID, **Secret Access Key, default region (e.g., us-west-2), and output format (json). *Note: Ensure your system clock is synchronized to prevent AWS Signature Expired errors.
### 3. Install Python Dependencies
Install the required libraries:
bash
pip install requests beautifulsoup4 boto3 selenium


##  Running the Scrapers
### Part 1: Run Static Scraper
 1. Ensure your DynamoDB table (QuotesTable) is created with Quote_id (String, Partition Key) and Author_name (String, Sort Key).
 2. Execute the script:
   bash
   python scrapper.py
   
   
### Part 2: Run Dynamic Scraper
 1. Update the WebDriver executable path in the script to match your local environment (e.g., C:\WebDriver\msedgedriver.exe).
 2. Execute the script:
   bash
   python dynamic_scrapper.py
   
   
##  Verification
 1. Navigate to the *AWS Management Console*.
 2. Open *DynamoDB* -> *Tables* -> QuotesTable.
 3. Click *Explore items* to verify that scraped quotes, author names, tags, and timestamps have been stored successfully.
