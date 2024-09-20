import asyncio
from bs4 import BeautifulSoup
import aiohttp
import pandas as pd
import json

gpu_site_crawl = "https://www.techpowerup.com/gpu-specs/?ajaxsrch="

async def fetch_gpus(session, site):
    async with session.get(site) as response:
        return await response.text()

async def parse_gpu_specs(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    gpus = table.find_all('tr')

    gpu_specs = []
    for gpu in gpus:
        gpu_specs.append([spec for spec in gpu.text.split('\n') if spec])

    return gpu_specs

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch_gpus(session, gpu_site_crawl)
        gpu_specs = await parse_gpu_specs(html)

    df = pd.DataFrame(gpu_specs[1:], columns=gpu_specs[0])

    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
    with open('gpu_specs.json', 'w') as f:
        json.dump(json_list, f)
        

asyncio.run(main())