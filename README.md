# Fossil Men's Watches Scraper

This Python script scrapes product data from the Fossil website's men's watches section and saves it to a CSV file. It utilizes HTTP requests and HTML parsing to extract information such as product titles and prices.

## Modules Required

Before running the program, ensure you have the following modules installed:

- **httpx**: A fully featured HTTP client for Python 3, which provides sync and async APIs, and support for HTTP/2.
- **selectolax**: A fast, flexible, and easy-to-use HTML parser.
- **dataclasses**: A module that provides a decorator and functions for automatically adding special methods to classes.

You can install these modules via pip using the following commands:

```bash
pip install httpx
pip install selectolax
```

## Usage

1. **Scraping HTML**: The program makes HTTP requests to the Fossil website's men's watches section for each page and retrieves the HTML content.

2. **Parsing Products**: It then parses the HTML content to extract product titles and prices using CSS selectors.

3. **Saving to CSV**: The extracted product data is stored in a CSV file named `fossil_data.csv`.

4. **Pagination**: The script iterates through multiple pages (from 1 to 9) to scrape more products.

## Example

Here's a brief example of how to use the program:

```python
# Importing necessary libraries
import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv

# Define dataclass for Product
@dataclass
class Product:
    title: str
    price: str

# Function to make HTTP request and get HTML content
def get_html(page):
    url = f"https://www.fossil.com/en-gb/watches/mens-watches/?&page={page}"
    resp =  httpx.get(url) 
    return HTMLParser(resp.text)

# Function to parse products from HTML
def parse_products(html):
    products = html.css("div.product-tile")
    results = []
    for item in products:
        new_item = Product(
            title=item.css_first("div.pdp-link").text().strip(),
            price=item.css_first("div.prices-container span.value").text().strip(),
        )
        results.append(asdict(new_item))
    return results

# Function to write products to CSV
def to_csv(res):
    with open("fossil_data.csv", "a" ) as f:  
        writer = csv.DictWriter(f, fieldnames=["title", "price",])
        writer.writerows(res)

# Main function to orchestrate the scraping process
def main():
    for p in range(1, 10):
        html = get_html(p)
        print(html.css_first("title").text())
        res = parse_products(html)
        to_csv(res)

# Execute main function
if __name__ == "__main__":
    main()
```

## Note

- Ensure you have the correct URL for the Fossil men's watches section. Adjust the URL if necessary.
- This script assumes a specific HTML structure on the Fossil website. Any changes to the website's structure may require modifications to the CSS selectors used in the parsing process.

Happy scraping! 🕵️‍♂️👨‍💻
