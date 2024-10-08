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
import datetime

UNKNOW_CASE = ["Never Released", "Unknown", "N/A", "TBD", "TBA"]
CPU_SITE_CRAWL = "https://www.techpowerup.com/cpu-specs/"


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

async def parseCpuCodename():
    cpu_code_name = []
    async with aiohttp.ClientSession() as session:
        html,status = await fetch(session, CPU_SITE_CRAWL)     
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='codename')
    codenames = table.find_all('option')

    for codename in codenames:
        cpu_code_name.append(codename['value'])
    
    return cpu_code_name

async def crawl(cpu_code_name):
    
    cpu_specs = []
    for codename in cpu_code_name :
        if not codename :
            continue
        print(codename)
        async with aiohttp.ClientSession() as session:
            html,status = await fetch(session, CPU_SITE_CRAWL + "?codename=" + codename)
        count = 0
        while status != 200:
            count += 1
            time.sleep(30)
            async with aiohttp.ClientSession() as session:
                html,status = await fetch(session, CPU_SITE_CRAWL + "?codename=" + codename)
            if count == 4:
                print("Try to refresh the page and solve the captcha")
                time.sleep(900)
                count = 0
                
        current_cpus = await parseCpuSpecs(html)
        for cpu in current_cpus[2:]:
            if len(cpu) < 9:
                cpu.append("Unknown")
                cpu_specs.append(cpu)
    return cpu_specs
    

def parseDate(date):
    parsed_date = parse(date)
    if parsed_date.day is not None:
        return parsed_date.strftime('%Y-%m-%d')
    else:
        return parsed_date.strftime('%Y-%m')

def main():

    cpu_code_name = asyncio.run(parseCpuCodename())
    cpu_specs = asyncio.run(crawl(cpu_code_name))
    data = [['Name', 'Codename', 'Cores', 'Clock', 'Socket', 'Process', 'L3 Cache', 'TDP', 'Released']]

    for each in cpu_specs:
        for cpu in each[1:]:
            if len(cpu) < 9:
                cpu.append("Unknown")
            data.append(cpu)


    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[~df["Released"].isin(UNKNOW_CASE)]
    df["Released Date"] = df["Released"].apply(parseDate)
    df = df.sort_values(by="Released Date", ascending=False)
    df = df.reset_index(drop=True)
    df = df.drop(columns=["Released Date"])

    data = df.to_dict(orient='records')
    with open("cpu_specs.json", "w") as f:
        f.write(json.dumps(data, indent=2))



if __name__ == '__main__':
    main()
