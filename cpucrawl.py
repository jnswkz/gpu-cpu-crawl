import asyncio
from bs4 import BeautifulSoup
import aiohttp
import pandas as pd
import numpy as np
import time
import ast
import json
from dateparser import parse
from numpy import argsort
from natsort import index_natsorted
import datetime

cpu_code_name = []
UNKNOW_CASE = ["Never Released", "Unknown", "N/A", "TBD", "TBA"]

async def fetch(session, site):
    async with session.get(site) as response:
        print(response.status)
        return await response.text(), response.status
    
async def parseCpuSpecs(html):    
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='list')
    cpus = table.find_all('tr')

    cpu_specs = []
    for cpu in cpus:
        cpu_specs.append([spec for spec in cpu.text.split('\n') if spec])
    return cpu_specs

async def crawl():
    
    CPU_SITE_CRAWL = "https://www.techpowerup.com/cpu-specs/?codename="

    cpu_specs = []
    current = 1
    f = open("./txt/cpu_specs"+current+".txt", "w")
    async with aiohttp.ClientSession() as session:
        for current_codename in cpu_code_name:
            for cpu in current_codename:
                site = CPU_SITE_CRAWL + cpu
                html, status = await fetch(session, site)
                if status == 200:
                    cpu_specs = await parseCpuSpecs(html)
                    f.write(cpu_specs.__str__())
                    f.write("\n")
                    print("finished: ", cpu)
                else:
                    count = 0 
                    while status != 200:
                        time.sleep(30)
                        if count == 3:
                            break
                        html, status = await fetch(session, site)
                        if status == 200:
                            await parseCpuSpecs(html)
                            f.write(cpu_specs.__str__())
                            f.write("\n")
                            break
                        count += 1
            current += 1
            time.sleep(60)

def parseDate(date):
    parsed_date = parse(date)
    if parsed_date.day is not None:
        return parsed_date.strftime('%Y-%m-%d')
    else:
        return parsed_date.strftime('%Y-%m')

def main():
    # asyncio.run(crawl())
    data = [['Name', 'Codename', 'Cores', 'Clock', 'Socket', 'Process', 'L3 Cache', 'TDP', 'Released']]
    for nbfile in range(1, 7):
        with open("./txt/cpu_specs"+str(nbfile)+".txt") as f:
            while line := f.readline():
                l = ast.literal_eval(line)
                for cpu in l[2:]:
                    if len(cpu) < 9:
                        cpu.append("Unknown")
                    data.append(cpu)
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[~df["Released"].isin(UNKNOW_CASE)]
    df["Released Date"] = df["Released"].apply(parseDate)
    df = df.sort_values(by="Released Date", ascending=False)
    df = df.reset_index(drop=True)
    df = df.drop(columns=["Released Date"])

    df.to_json('cpu_specs.json', orient='records')


if __name__ == '__main__':
    with open("cpu_codename.json") as f:
        cpu_code_name = json.load(f)
    main()
