import asyncio
from bs4 import BeautifulSoup
import aiohttp
import json

cpu_code_name = []

site = "https://www.techpowerup.com/cpu-specs/"

async def fetch(session, site):
    async with session.get(site) as response:
        return await response.text()

async def parse_cpu_code_name():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, site) 
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='codename')
    codenames = table.find_all('option')

    cur = 0
    current_codename = []
    for codename in codenames:
        cur += 1
        current_codename.append(codename['value'])
        if cur == 40:
            cpu_code_name.append(current_codename)
            current_codename = []
    
    cpu_code_name.append(current_codename)

asyncio.run(parse_cpu_code_name())
with open("cpu_codename.json","w") as f:
    f.write(json.dumps(cpu_code_name))
    

