import asyncio
from bs4 import BeautifulSoup
import aiohttp
import pandas as pd
import numpy as np
import time
import ast
import json

cpu_code_name = []

async def fetch(session, site):
    async with session.get(site) as response:
        print(response.status)
        return await response.text(), response.status
    
async def parse_cpu_specs(html):    
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='list')
    cpus = table.find_all('tr')

    cpu_specs = []
    for cpu in cpus:
        cpu_specs.append([spec for spec in cpu.text.split('\n') if spec])
    return cpu_specs

async def crawl():
    
    cpu_site_crawl = "https://www.techpowerup.com/cpu-specs/?codename="

    cpu_specs = []
    current = 1
    f = open("./txt/cpu_specs"+current+".txt", "w")
    async with aiohttp.ClientSession() as session:
        for current_codename in cpu_code_name:
            for cpu in current_codename:
                site = cpu_site_crawl + cpu
                html, status = await fetch(session, site)
                if status == 200:
                    cpu_specs = await parse_cpu_specs(html)
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
                            await parse_cpu_specs(html)
                            f.write(cpu_specs.__str__())
                            f.write("\n")
                            break
                        count += 1
            current += 1
            time.sleep(60)
    
def main():
    asyncio.run(crawl())
    data = [['Name', 'Codename', 'Cores', 'Clock', 'Socket', 'Process', 'L3 Cache', 'TDP', 'Released']]
    for nbfile in range(1, 7):
        with open("./txt/cpu_specs"+str(nbfile)+".txt") as f:
            while line := f.readline():
                l = ast.literal_eval(line)
                for cpu in l[2:]:
                    data.append(cpu)
    # with open('cpu_specs.json', 'w') as f:
    #     json.dump(data, f)
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_json('cpu_specs.json', orient='records')
if __name__ == '__main__':
    with open("cpu_codename.json") as f:
        cpu_code_name = json.load(f)
    main()
