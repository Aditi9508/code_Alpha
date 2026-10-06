import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/"

books_data = []

TOTAL_PAGES = 5

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

for page_number in range(1, TOTAL_PAGES + 1):

    if page_number == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}catalogue/page-{page_number}.html"

    print(f"Scraping Page {page_number}...")

    response = requests.get(url, headers=headers, timeout=10)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:

        title = book.h3.a.get("title")

        price = book.find(
            "p", class_="price_color"
        ).text.strip()

        availability = book.find(
            "p", class_="instock availability"
        ).text.strip()

        rating_class = book.find(
            "p", class_="star-rating"
        ).get("class")

        rating_word = rating_class[1]
        rating = rating_map.get(rating_word)

        relative_url = book.h3.a.get("href")

        product_url = BASE_URL + "catalogue/" + relative_url.replace(
            "../", ""
        )

        books_data.append({
            "Book Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability,
            "Product URL": product_url
        })

    time.sleep(1)

df = pd.DataFrame(books_data)

df.drop_duplicates(
    subset=["Book Title"],
    inplace=True
)

df.to_csv(
    "books_dataset.csv",
    index=False,
    encoding="utf-8"
)

print("\nScraping completed successfully!")

print(f"Total books collected: {len(df)}")

print("\nFirst 10 records:")
print(df.head(10))

print("\nDataset information:")
print(df.info())

print("\nRating distribution:")
print(df["Rating"].value_counts().sort_index())

print("\nCSV file saved as: books_dataset.csv")