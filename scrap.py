import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.amazon.in/s"
search_query = "bags"
pages_to_scrape = 20
products_to_scrape = 200

data = []

for page in range(1, pages_to_scrape + 1):
    params = {
        "k": search_query,
        "page": page,
        "ref": f"sr_pg_{page}"
    }

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    product_list = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in product_list:
        if len(data) >= products_to_scrape:
            break

        product_url = "https://www.amazon.in" + product.find("a", {"class": "a-link-normal"})["href"]
        product_name = product.find("span", {"class": "a-size-medium"}).text.strip()
        product_price = product.find("span", {"class": "a-offscreen"}).text.strip()

        rating_element = product.find("span", {"class": "a-icon-alt"})
        if rating_element:
            rating = rating_element.text.strip().split()[0]
        else:
            rating = "N/A"

        review_count_element = product.find("span", {"class": "a-size-base"})
        if review_count_element:
            review_count = review_count_element.text.strip().split()[0]
        else:
            review_count = "0"

        # Additional scraping for each product URL
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, "html.parser")

        description_element = product_soup.find("div", {"id": "feature-bullets"})
        if description_element:
            description = description_element.get_text(separator=" ").strip()
        else:
            description = "N/A"

        asin_element = product_soup.find("th", text="ASIN")
        if asin_element:
            asin = asin_element.find_next("td").text.strip()
        else:
            asin = "N/A"

        product_description_element = product_soup.find("div", {"id": "productDescription"})
        if product_description_element:
            product_description = product_description_element.get_text(separator=" ").strip()
        else:
            product_description = "N/A"

        manufacturer_element = product_soup.find("a", {"id": "bylineInfo"})
        if manufacturer_element:
            manufacturer = manufacturer_element.text.strip()
        else:
            manufacturer = "N/A"

        # Append the scraped data to the list
        data.append([product_name, product_url, product_price, rating, review_count, description, asin, product_description, manufacturer])

        if len(data) >= products_to_scrape:
            break

# Export the data to a CSV file
with open("product_data.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Product Name", "Product URL", "Product Price", "Rating", "Review Count", "Description", "ASIN", "Product Description", "Manufacturer"])
    writer.writerows(data)

print("Data exported successfully!")
