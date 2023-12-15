import re, asyncio, os, random, aiofiles
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from zenrows import ZenRowsClient # Proxy
from tqdm import tqdm

BASE_URL = "https://www.habitaclia.com/alquiler-distrito_eixample-barcelona.html"
# Pre_url = BASE_URL + "alquiler-viviendas/barcelona-barcelona"

os.system('cls')
# client = ZenRowsClient("f96457adf49d2038a190f98731285fa41cc17efa")
client = ZenRowsClient("55b97c99648a98ca7a4142d56622d05cfe773c9a")

async def extract_href(element):
    await asyncio.sleep(0)  # Yield control to the event loop
    a_tag = element.find('a')
    if a_tag:
        return a_tag.get('href')
    return None


async def extract_price(html) -> float:
    # Using a regular expression to find the price pattern in the HTML string
    match = re.search(r'<span[^>]*itemprop="price"[^>]*>([^<]+)€</span>', html)
    if match:
        return float(match.group(1).strip().replace('.',''))
    return -1

async def save_content(content, filename=None):
    if filename is None:
        filename = f"File{random.randint(100, 1000)}.txt"
    async with aiofiles.open(os.path.join(os.getcwd(), "results", filename), "w+") as f:
        await f.write(str(content))
        
    print("Content printed succsesfully!")

async def get_features(html):
    await asyncio.sleep(0)
    
    # Extract square meters
    m2 = None
    match_m2 = re.search(r'<strong>(\d+,\d+|\d+)</strong>\s*m<sup>2</sup>', html)
    if match_m2:
        m2 = float(match_m2.group(1))

    # Extract number of bedrooms
    bedrooms = None
    match_bedrooms = re.search(r'<strong>(\d+)</strong>\s*hab.', html)
    if match_bedrooms:
        bedrooms = int(match_bedrooms.group(1))
    
    # Extract number of bathrooms
    bathrooms = None
    match_bathrooms = re.search(r'<strong>(\d+)</strong>\s*baños', html)
    if match_bathrooms:
        bathrooms = int(match_bathrooms.group(1))
    else:
        bathrooms = 1
        
    # Extract price per square meter
    price_m2 = None
    match_price_m2 = re.search(r'<strong>(\d+,\d+|\d+)</strong>\s*€/m<sup>2</sup>', html)
    if match_price_m2:
        price_m2 = float(match_price_m2.group(1).replace(',', '.'))

    return m2, bedrooms, bathrooms, price_m2

async def get_other_features(html):
    if html is None:
        return -1, False
    
    soup = BeautifulSoup(str(html), "lxml", from_encoding="utf-8")
    text_content = soup.get_text(separator=" ", strip=True)

    year_of_construction = -1
    air_conditioner = False

    result_year = re.search(r'Año construcción (\d+)', text_content)
    search_air_conditioner = re.search(r'Aire acondicionado', text_content, re.IGNORECASE)

    if result_year:
        year_of_construction = int(result_year.group(1))
    if search_air_conditioner:
        air_conditioner = True

    return year_of_construction, air_conditioner

async def scrap_single_page(url):
    soup = BeautifulSoup(client.get(url).text, "lxml")

    span_price = soup.find_all('div', class_="price", )
    span_features = soup.find_all('ul', class_="feature-container")
    span_neighborhood = soup.find('a', class_="jqVerMapaZonaTooltip link-map-location")
    span_addit_info = soup.find_all('article', class_="has-aside")

    # Extract each value
    m2, bedrooms, bathrooms, price_m2 = await get_features(str(span_features))
    price = await extract_price(str(span_price))
    title_element = soup.find('h1')
    title = title_element.text if title_element else "Not found"
    city = title.split(" ")[-1] if title != "Not found" else "Not found"
    neighborhood = span_neighborhood.text.strip() if span_neighborhood else "Not found"
    year_of_construction, air_conditioner = await get_other_features(span_addit_info)

    return url, title, city, neighborhood, price, m2, price_m2, bedrooms, bathrooms, year_of_construction, air_conditioner



async def scrap_webs():
    urls = []
    data_frame_of_houses = pd.DataFrame(columns=['url','title','city','neighborhood','price_per_month','m2','price_m2','bedrooms','bathrooms','year_of_construction','air_conditioner'], index=None)

    for i in tqdm(range(50)):
        e = f"-{i}" if i >= 1 else ""
        url_base = f"https://www.habitaclia.com/alquiler-barcelona{e}.html"

        # Select links in each page
        soup = BeautifulSoup(client.get(url_base).text, "lxml")
        h3_elements = soup.find_all('h3', class_="list-item-title")
        urls = await asyncio.gather(*(extract_href(element) for element in h3_elements))

        
        tasks = [scrap_single_page(url) for url in urls]
        result = await asyncio.gather(*tasks)

        for row in result:
            # Append data into the DataFrame
            print(row)
            data_frame_of_houses = data_frame_of_houses._append(pd.Series(row, index=data_frame_of_houses.columns), ignore_index=True)


    return data_frame_of_houses



async def main():
    data_frame_of_houses = await scrap_webs()
    print(data_frame_of_houses)
    data_frame_of_houses.to_csv(os.path.join(os.getcwd(), "results", "Result2_0.csv"), index=False, encoding="utf-8-sig")


asyncio.run(main())








