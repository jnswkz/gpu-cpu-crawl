import asyncio
from bs4 import BeautifulSoup
import aiohttp
import pandas as pd
import json
from dateparser import parse


GPU_SITE_CRAWL = "https://www.techpowerup.com/gpu-specs/?ajaxsrch="
UNKNOW_CASE = ["Never Released", "Unknown", "N/A", "TBD", "TBA"]

async def fetchGpus(session, site):
    async with session.get(site) as response:
        return await response.text()

async def parseGpuSpecs(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    gpus = table.find_all('tr')

    gpu_specs = []
    for gpu in gpus:
        gpu_specs.append([spec for spec in gpu.text.split('\n') if spec])

    return gpu_specs

def parseDate(date):
    parsed_date = parse(date)
    if parsed_date.day is not None:
        return parsed_date.strftime('%Y-%m-%d')
    else:
        return parsed_date.strftime('%Y-%m')

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetchGpus(session, GPU_SITE_CRAWL)
        gpu_specs = await parseGpuSpecs(html)

    df = pd.DataFrame(gpu_specs[1:], columns=gpu_specs[0])
    df = df[~df["Released"].isin(UNKNOW_CASE)]
    df["Released Date"] = df["Released"].apply(parseDate)
    df = df.sort_values(by="Released Date", ascending=False)
    df = df.reset_index(drop=True)
    df = df.drop(columns=["Released Date"])
    # print(df)
    # df.to_csv('gpu_specs.csv', index=False)

    df.to_json('gpu_specs.json', orient='records')
        

asyncio.run(main())