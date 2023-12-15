import pandas as pd
import numpy as np
import asyncio, os, aiofiles
from sklearn.preprocessing import LabelEncoder


cls = lambda: os.system('cls'); cls()
df = pd.read_csv("https://raw.githubusercontent.com/ElStevenn/PropertyPricePredictor/main/datasets/encoded_labels.csv", index_col=False, delimiter=",")
Neight_encoder =  LabelEncoder()

async def read_urls_from_file():
    async with aiofiles.open('not_founds.txt', 'r') as f:
        content = await f.read()

    lines = content.splitlines()
    urls = []
    
    for line in lines:
        # Remove brackets and split by comma
        urls_in_line = line[1:-1].split(', ')
        for url in urls_in_line:
            # Remove quotes around each URL
            urls.append(url.strip('\'"'))

    return urls

def generate_encoderd_labels():
    pd_reducted = df[['url','neighborhood','price_per_month','m2','price_m2','bedrooms', 'bathrooms']]

    df_encoder = pd.read_csv("neighborhood_sorted_codificated.csv")

    mapping_dict = dict(zip(df_encoder['neighborhood'], df_encoder['cat']))
    pd_reducted['encoded_neighborhood'] = pd_reducted['neighborhood'].map(mapping_dict)

    pd_reducted.drop(columns=['neighborhood'], index=1, inplace=True)
    print(pd_reducted)

    pd_reducted.to_csv("encoded_labels.csv", encoding="utf-8-sig", index=False)




print(df)