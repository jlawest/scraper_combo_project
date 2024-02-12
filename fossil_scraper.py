import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv

@dataclass

# create class that populates it with all the objects we'll need.
class Product:
    title: str
    price: str

    

# this will make the request to the server of the url and return as text the data scraped. 
def get_html(page):
    url = "https://www.fossil.com/en-gb/watches/mens-watches/?&page={page}"
    resp =  httpx.get(url) 
    return HTMLParser(resp.text)

# specifying what html element we want scraped from the site. This is the title element for each product. 
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


def to_csv(res):
    with open("fossil_price_data.csv", "a" ) as f:  
        writer = csv.DictWriter(f, fieldnames=["title", "price",])
        writer.writerows(res)
    
    
# for loop that will iterate through the pages of the site we have scraped data from. 
def main():
    for p in range(1,10):
        html = get_html(p)
        print(html.css_first("title").text())
        res = parse_products(html)
        to_csv(res)
        
#
if __name__ == "__main__":
    main()
    
    
    
    
    