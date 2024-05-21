import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f'Error fetching URL {url}: {e}')
        return None

def extract_product_urls(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    product_urls = []
    product_links = soup.find_all('a', href=True)
    print(f"Found {len(product_links)} links")
    for link in product_links:
        href = link['href']
        print(f"Checking link: {href}")
        if '/product/' in href:
            full_url = urljoin(base_url, href)
            product_urls.append(full_url)
            print(f"Added product URL: {full_url}")
    return product_urls

def remove_duplicates(urls):
    # Remove URLs with '/alternatives' and keep only unique URLs
    filtered_urls = [url for url in urls if '/alternatives' not in url]
    unique_urls = list(set(filtered_urls))
    print(f"Removed duplicates and filtered alternatives, {len(unique_urls)} unique URLs remain")
    return unique_urls

def save_to_excel(urls, filename):
    df = pd.DataFrame(urls, columns=['Product URL'])
    df.to_excel(filename, index=False)
    print(f'Saved {len(urls)} URLs to {filename}')

def main(catalog_url):
    html = fetch_html(catalog_url)
    if html:
        base_url = catalog_url.split('/catalog')[0]
        product_urls = extract_product_urls(html, base_url)
        product_urls = remove_duplicates(product_urls)
        output_excel_file = f'ProductURL_{datetime.now().strftime("%Y%m%d%H%M")}.xlsx'
        save_to_excel(product_urls, output_excel_file)

if __name__ == '__main__':
    catalog_url = input("Enter the catalog URL: ")
    main(catalog_url)