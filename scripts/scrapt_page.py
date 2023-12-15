import re, asyncio, os, random, aiofiles
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from zenrows import ZenRowsClient # Proxy
from tqdm import tqdm

cls = lambda: os.system('cls'); cls()

class proxy:
    def __init__(self):
        self.client = ZenRowsClient("55b97c99648a98ca7a4142d56622d05cfe773c9a")

class Scrap_Habitaclia_Page(proxy):
    """
    Output: url | title_of_anouncement | Neighborhood | price per month | m2 of the house | price per m2 | bedrooms | bathrooms | Age of construction | Air_aconditionair
    """

    def __init__(self):
        super().__init__()
    
    async def extract_price(self, html) -> float:
        # Using a regular expression to find the price pattern in the HTML string
        match = re.search(r'<span[^>]*itemprop="price"[^>]*>([^<]+)€</span>', html)
        if match:
            return float(match.group(1).strip().replace('.',''))
        return -1

    async def save_content(self, content, filename=None):
        if filename is None:
            filename = f"File{random.randint(100, 1000)}.txt"
        async with aiofiles.open(os.path.join(os.getcwd(), "results", filename), "w+") as f:
            await f.write(str(content))
            
        print("Content printed succsesfully!")

    async def study_how_many_bedrooms(self, text: str) -> int or None:
        number_words_to_digits = {
            'una': 1, 'un': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5,
            'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10
        }

        # Set up the patterns
        room_pattern = re.compile(
            r'(\d+|una|un|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\s+(habitación(?:es)?|dormitorio(?:s)?)',
            re.IGNORECASE
        )
        matches = room_pattern.findall(text)

        # Process the matches
        if matches:

            match = matches[0]
            num_string = match[0].lower()

            if num_string.isdigit():
                num_rooms = int(num_string)
            else:
                num_rooms = number_words_to_digits.get(num_string, None)

            return num_rooms
        else:
            return None
    
    async def study_how_many_bathrooms(self, text: str) -> int or None:
        # End this!! it's so important
        number_words_to_digits = {
            'una': 1, 'un': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5,
            'seis': 6, 'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10
        }

        bathroom_pattern = re.compile(
            r'(\d+|una|un|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\s+(baño(?:s)?|lavabo(?:s)?)', 
            re.IGNORECASE
        )
            
        matches = bathroom_pattern.findall(text)
        if matches:
            match = matches[0]
            num_string = match[0].lower()

            if num_string.isdigit():
                num_rooms = int(num_string)
            else:
                num_rooms = number_words_to_digits.get(num_string, None)
            
            return num_rooms
        else:
            return None

    async def get_features(self, html, price, soup: BeautifulSoup):
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
        else:
            text = soup.find_all('p', class_="detail-description")
            result = await self.study_how_many_bedrooms(str(text))
            if result:
                bedrooms = result
            else:
                bedrooms = 1 if price < 1600 else 2
                
        # Extract number of bathrooms
        bathrooms = None
        match_bathrooms = re.search(r'<strong>(\d+)</strong>\s*baños', html)
        if match_bathrooms:
            bathrooms = match_bathrooms.group(1)
        else:
            bathrooms = 1 if price < 1600 else 2
            
        # Extract price per square meter
        price_m2 = None
        match_price_m2 = re.search(r'<strong>(\d+,\d+|\d+)</strong>\s*€/m<sup>2</sup>', html)
        if match_price_m2:
            price_m2 = float(match_price_m2.group(1).replace(',', '.'))

        return m2, bedrooms, bathrooms, price_m2


    async def get_other_features(self,html):
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

    async def scrap_single_page(self, url):
        soup = BeautifulSoup(self.client.get(url).text, "lxml")

        span_price = soup.find_all('div', class_="price", )
        span_features = soup.find_all('ul', class_="feature-container")
        span_neighborhood = soup.find('a', class_="jqVerMapaZonaTooltip link-map-location")
        span_addit_info = soup.find_all('article', class_="has-aside")

        # Extract each value
        
        price = await self.extract_price(str(span_price))
        m2, bedrooms, bathrooms, price_m2 = await self.get_features(str(span_features), price, soup)
        title_element = soup.find('h1')
        title = title_element.text if title_element else "Not found"
        city = title.split(" ")[-1] if title != "Not found" else "Not found"
        neighborhood = span_neighborhood.text.strip() if span_neighborhood else "Not found"
        year_of_construction, air_conditioner = await self.get_other_features(span_addit_info)

        return url, title, city, neighborhood, price, m2, price_m2, bedrooms, bathrooms, year_of_construction, air_conditioner

class scrapt_rentola(proxy):
    """
    output: 
    """
    URL_BASE = "https://rentola.es/alquiler/"
    
    def __init__(self):
        super().__init__()
    
    async def extract_main_features(self, html):
        pattern_bathroom = re.compile(r'<div class="f-column">(\d+) (?:cuarto(?:s)? de baño(?:s)?)</div>', re.IGNORECASE)
        pattern_bedroom = re.compile(r'<div class="f-column">(\d+)\s(?:dormitorio(?:s)?|habitacion(?:es)?)', re.IGNORECASE)
        pattern_m2 = re.compile(r'<div class="f-column">(\d+,\d+|\d+)\sm<sup>2</sup></div>', re.IGNORECASE)

        bathrooms = pattern_bathroom.findall(html)
        bedrooms = pattern_bedroom.findall(html)
        m2 = pattern_m2.findall(html)
        
     

        return m2[0] or None, bedrooms[0] or None, bathrooms[0] or None

    async def main(self, url):
        soup =  BeautifulSoup(self.client.get(url).text, "lxml")
        
        span_features = soup.find('div', class_="lower-content-rows")
        price = soup.find('span', class_="amount").text[:-2] or None
        city = str((soup.find('div', class_="location").text).split(",")[-1]).strip()
        #price = re.compile(r'<span class="amount">(\d+,\d+|\d+)\s€</span>', re.IGNORECASE).findall(str(soup.find_all('span', class_="amount")))[0] or None  
        m2, bedrooms, bathrooms = await self.extract_main_features(str(span_features))
        price_m2 = soup.find('span', class_="data")
        title = soup.find('div', class_="title").text.strip()
        neighborhood = soup.find() # End this shit please
        year_of_construction = None
        air_conditioner = None
        return url, title,neighborhood, price, city, m2, price_m2, bedrooms, bathrooms, air_conditioner
        

class scrapt_any_page(proxy):
    """
    output: 
    """
    def __init__(self):
        super().__init__()
    
    async def search_m2(self, divs_span):
        pattern = re.compile(r'(/d+)m', re.IGNORECASE)
       

    async def read_divs(self, div_span):
        return div_span

    async def main(self, url):
        soup = BeautifulSoup(self.client.get(url).text, "lxml")

        body = soup.find('body')
        divs = await self.read_divs(body.find('div'))

        m2 = self.search_m2(divs_span)
        return m2
        

class scrapt_page4(proxy):
    """
    output: 
    """
    def __init__(self):
        super().__init__()
    


    def main():
        pass



class scrapt_page6(proxy):
    """
    output: 
    """
    def __init__(self):
        super().__init__()
    


    async def main():
        pass



if __name__ == "__main__":
    url = "https://www.habitaclia.com/alquiler-piso-espectacular_vivienda_con_2_grandes_terrazas_y_parking_plaza_d_adria_8_sant_gervasi_galvany-barcelona-i4542004335075.htm?f=&geo=p&from=list&lo=55"
    habitaclia = Scrap_Habitaclia_Page()

    result = asyncio.run(habitaclia.scrap_single_page(url))   
    print(result)
