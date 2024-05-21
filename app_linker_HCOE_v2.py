import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random

# Function to fetch HTML content
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        st.error(f'Error fetching URL {url}: {e}')
        return None

# Function to extract product URLs
def extract_product_urls(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    product_urls = []
    product_links = soup.find_all('a', href=True)
    st.write(f"Found {len(product_links)} links")
    for link in product_links:
        href = link['href']
        if '/product/' in href:
            full_url = urljoin(base_url, href)
            product_urls.append(full_url)
    return product_urls

# Function to remove duplicates
def remove_duplicates(urls):
    filtered_urls = [url for url in urls if '/alternatives' not in url]
    unique_urls = list(set(filtered_urls))
    st.write(f"Removed duplicates and filtered alternatives, {len(unique_urls)} unique URLs remain")
    return unique_urls

# Function to save URLs to Excel
def save_to_excel(urls, filename):
    df = pd.DataFrame(urls, columns=['Product URL'])
    df.to_excel(filename, index=False)
    st.write(f'Saved {len(urls)} URLs to {filename}')

# Streamlit app
st.title('McKesson Product URL Extractor')
st.write("Proof of concept for a tool to extract product URLs from McKesson's website and save them to an Excel file. Uses BeautifulSoup (not AI). Developed in 1 day by Ivan for Thomas & Jack (HCOE).")

# Input for catalog URL with an example
catalog_url = st.text_input("Enter the catalog URL (e.g., https://mms.mckesson.com/catalog?node=25974031+5589993&pageSize=100&pageOffset=1)")

# Button to start extraction
if st.button('Extract URLs'):
    if catalog_url:
        html = fetch_html(catalog_url)
        if html:
            base_url = catalog_url.split('/catalog')[0]
            product_urls = extract_product_urls(html, base_url)
            product_urls = remove_duplicates(product_urls)
            output_excel_file = f'ProductURL_{datetime.now().strftime("%Y%m%d%H%M")}.xlsx'
            save_to_excel(product_urls, output_excel_file)
            
            # Display a table of 10 random sample URLs
            if len(product_urls) > 10:
                sample_urls = random.sample(product_urls, 10)
            else:
                sample_urls = product_urls
            st.write("Sample URLs:")
            st.table(pd.DataFrame(sample_urls, columns=['Product URL']))
            
            # Provide download link for the output file
            with open(output_excel_file, "rb") as file:
                btn = st.download_button(
                    label="Download Excel",
                    data=file,
                    file_name=output_excel_file,
                    mime="application/vnd.ms-excel"
                )
    else:
        st.error("Please enter a valid catalog URL.")

# Running the app: streamlit run app_link_extractor_HCOE_v2.py
# Running the app: streamlit run app_link_extractor_HCOE_v2.py