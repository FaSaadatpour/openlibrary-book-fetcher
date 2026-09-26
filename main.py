import requests
import csv
from typing import List, Dict

API_URL = "https://openlibrary.org/search.json"
LIMIT = 200
OUTPUT_FILE = "books.csv"
HEADERS = {
    "User-Agent": "BookFetcher/1.0 (student-project@example.com)"
}


def fetch_books(limit: int = 200) -> List[Dict]:
    params = {
        "q": "subject:fiction",
        "limit": limit,
        "fields": "title,author_name,first_publish_year,key,edition_count"
    }
    
    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=20)
    response.raise_for_status()
    
    data = response.json()
    return data.get("docs", [])


def filter_books(books: List[Dict]) -> List[Dict]:
    filtered = []
    for book in books:
        year = book.get("first_publish_year")
        if year and isinstance(year, int) and 2001 <= year <= 2026:
            filtered.append(book)
    return filtered


def sort_books(books: List[Dict]) -> List[Dict]:
    return sorted(books, key=lambda x: x.get("first_publish_year", 0), reverse=True)


def save_to_csv(books: List[Dict], filename: str = OUTPUT_FILE):
    if not books:
        print("No books found after filtering.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow(["Title", "Authors", "First Publish Year", "Edition Count", "Open Library Key"])
        
        for book in books[:50]:
            title = book.get("title", "N/A")
            authors = ", ".join(book.get("author_name", ["Unknown"]))
            year = book.get("first_publish_year", "N/A")
            editions = book.get("edition_count", "N/A")
            key = book.get("key", "N/A")
            
            writer.writerow([title, authors, year, editions, key])
    
    print(f"{min(len(books), 50)} books successfully saved to '{filename}'.")


def main():
    print("Fetching books from Open Library...")
    
    try:
        books = fetch_books(LIMIT)
        print(f"{len(books)} books fetched.")
        
        filtered = filter_books(books)
        print(f"{len(filtered)} books published after 2000 found.")
        
        sorted_books = sort_books(filtered)
        save_to_csv(sorted_books)
        
    except requests.exceptions.RequestException as e:
        print("Error connecting to the API:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()