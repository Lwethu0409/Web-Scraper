import boto3
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


# 1. Connect to DynamoDB using your configured AWS credentials
dynamodb = boto3.resource("dynamodb")

quotes_table = dynamodb.Table("QuotesTable")
movies_table = dynamodb.Table("MoviesTable")


# 2. Retrieve all records from a DynamoDB table
def get_all_records(table):

    records = []
    response = table.scan()

    records.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:

        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )

        records.extend(response.get("Items", []))

    return records


# 3. Retrieve data from both tables
print("Retrieving data from DynamoDB...")

quotes = get_all_records(quotes_table)
movies = get_all_records(movies_table)

print("Quotes retrieved:", len(quotes))
print("Movies retrieved:", len(movies))


# 4. Convert records into Pandas DataFrames
quotes_df = pd.DataFrame(quotes)
movies_df = pd.DataFrame(movies)


# ==========================================
# PART A: QUOTES ANALYSIS
# ==========================================

print("\n========== QUOTES ANALYSIS ==========")

if not quotes_df.empty:

    print("Total quotes:", len(quotes_df))

    unique_authors = quotes_df["Author_Name"].nunique()
    print("Unique authors:", unique_authors)

    top_authors = quotes_df["Author_Name"].value_counts().head(5)

    print("\nTop 5 authors:")
    print(top_authors)

    # Author chart
    top_authors.sort_values().plot(
        kind="barh",
        title="Top 5 Authors by Number of Quotes",
        xlabel="Number of Quotes",
        ylabel="Author"
    )

    plt.tight_layout()
    plt.savefig("top_authors.png")
    plt.show()

    # Analyse tags
    all_tags = []

    for tags in quotes_df["Tags"].dropna():

        if isinstance(tags, list):
            all_tags.extend(tags)

        elif isinstance(tags, str):
            all_tags.extend(tags.split(","))

    tag_counts = Counter(
        tag.strip() for tag in all_tags if tag.strip()
    )

    print("\nTop 5 tags:")
    print(tag_counts.most_common(5))

    if tag_counts:

        top_tags = pd.Series(
            dict(tag_counts.most_common(5))
        ).sort_values()

        top_tags.plot(
            kind="barh",
            title="Most Common Quote Tags",
            xlabel="Frequency",
            ylabel="Tag"
        )

        plt.tight_layout()
        plt.savefig("top_quote_tags.png")
        plt.show()

else:
    print("No quote records found.")


# ==========================================
# PART B: MOVIES ANALYSIS
# ==========================================

print("\n========== MOVIES ANALYSIS ==========")

if not movies_df.empty:

    print("Total movies:", len(movies_df))

    movies_df["Awards"] = pd.to_numeric(
        movies_df["Awards"], errors="coerce"
    ).fillna(0)

    movies_df["Nominations"] = pd.to_numeric(
        movies_df["Nominations"], errors="coerce"
    ).fillna(0)

    total_awards = movies_df["Awards"].sum()
    total_nominations = movies_df["Nominations"].sum()

    print("Total awards:", int(total_awards))
    print("Total nominations:", int(total_nominations))

    # Top 5 movies by awards
    top_movies = movies_df.nlargest(5, "Awards")

    print("\nTop 5 movies by awards:")
    print(top_movies[["Movie_Title", "Awards", "Nominations"]])

    # Awards chart
    chart_data = top_movies.sort_values("Awards")

    chart_data.plot(
        x="Movie_Title",
        y=["Awards", "Nominations"],
        kind="bar",
        title="Movie Awards vs Nominations",
        ylabel="Count",
        xlabel="Movie"
    )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("movie_awards_analysis.png")
    plt.show()

else:
    print("No movie records found.")


# ==========================================
# PART C: FINAL SUMMARY
# ==========================================

print("\n========== PROJECT SUMMARY ==========")