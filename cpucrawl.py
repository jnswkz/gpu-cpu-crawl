import asyncio
from bs4 import BeautifulSoup
import aiohttp
import pandas as pd
import numpy as np
import time
import ast
import json

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
    # return cpu_specs

async def crawl():
    
    cpu_site_crawl = "https://www.techpowerup.com/cpu-specs/?codename="

    #cpu_code_name = ['Abu Dhabi', 'Agena', 'Albany', 'Alder Lake-H', 'Alder Lake-HX', 'Alder Lake-N', 'Alder Lake-P', 'Alder Lake-S', 'Alder Lake-U', 'Allendale', 'Amston Lake', 'Apollo Lake', 'Argon', 'Ariel', 'Arrandale', 'Arrow Lake-S', 'Athens', 'Banias', 'Barcelo', 'Barcelo-R', 'Barcelona', 'Barton', 'Bay Trail-I', 'Bay Trail-M', 'Bay Trail-T', 'Beema', 'Bergamo', 'Bloomfield', 'Brisbane', 'Bristol Ridge', 'Broadwell', 'Broadwell-DT', 'Broadwell-E', 'Broadwell-EP', 'Broadwell-H', 'Broadwell-U', 'Broadwell-Y', 'Brown Falcon', 'Budapest', 'CHA', 'CNA', 'CNC', 'CNQ', 'CNR', 'Callisto', 'Cannon Lake', 'Cannon Lake-Y', 'Cardinal', 'Carrizo', 'Cascade Lake-AP', 'Cascade Lake-SP', 'Cascade Lake-X', 'Cascades', 'Cascades-2M', 'Castle Peak', 'Cedar Mill', 'Cedarview', 'Centerton', 'Cezanne', 'Cezanne-U', 'Chagall', 'Chagall PRO', 'Clarkdale', 'Clarksfield']
    #cpu_code_name = ['Clawhammer', 'Clovertown', 'Clovertrail', 'Cloverview', 'Coffee Lake', 'Coffee Lake-H', 'Coffee Lake-HR', 'Coffee Lake-R', 'Coffee Lake-S WS', 'Coffee Lake-U', 'Colfax', 'Comet Lake', 'Comet Lake-H', 'Comet Lake-R', 'Comet Lake-U', 'Comet Lake-Y', 'Conroe', 'Conroe XE', 'Conroe-CL', 'Conroe-L', 'Cooper Lake-SP', 'Coppermine', 'Coppermine T', 'Coppermine-T', 'Cranford', 'Crystal Well', 'Crystalwell', 'Dali', 'Delhi', 'Dempsey', 'Deneb', 'Denmark', 'Desna', 'Diamondville', 'Dothan', 'Dragon Range', 'Drake', 'Egypt', 'Emerald Rapids', 'Excavator', 'Ezra', 'Ezra-T', 'Gainestown', 'Gallatin', 'Gemini Lake', 'Genoa', 'Genoa-X', 'Georgetown', 'Gladden', 'Godaveri']
    #cpu_code_name = ['Gracemont', 'Granite Ridge', 'Griffin', 'Gulftown', 'Harpertown', 'Haswell', 'Haswell-E', 'Haswell-EP', 'Haswell-EX', 'Haswell-ULT', 'Haswell-WS', 'Hawk Point', 'Heka', 'Hondo', 'Ice Lake-SP', 'Ice Lake-U', 'Ice Lake-W', 'Ice Lake-Y', 'Interlagos', 'Irwindale', 'Italy', 'Ivy Bridge', 'Ivy Bridge-E', 'Ivy Bridge-EN', 'Ivy Bridge-EP', 'Jasper Forest', 'Kabini', 'Kaby Lake', 'Kaby Lake G', 'Kaby Lake-DT', 'Kaby Lake-H', 'Kaby Lake-R', 'Kaby Lake-U', 'Kaby Lake-X', 'Kaveri', 'Kentsfield', 'Knights Corner', 'Knights Ferry', 'Knights Landing', 'Knights Mill', 'Kuma', 'Kyoto', 'Lakefield', 'Lancaster', 'Lima', 'Lincroft', 'Llano', 'Lucienne', 'Lunar Lake', 'Lynnfield', 'Magnolia', 'Magny-Cours', 'Manchester', 'Manila', 'Matisse', 'Matisse 2', 'Mendocino', 'Merom', 'Merom XE', 'Merom-L', 'Meteor Lake', 'Meteor Lake-PS', 'Milan', 'Milan-X', 'Naples', 'NewCastle', 'Newark', 'Nocona']
    #cpu_code_name = ['Northwood', 'Odessa', 'Ontario', 'Orion', 'Orleans', 'Palermo', 'Palomino', 'Paris', 'Paxville', 'Penryn', 'Penryn QC', 'Penryn QC XE', 'Penryn XE', 'Penryn-L', 'Penwell', 'Phoenix', 'Phoenix2', 'Picasso', 'Pineview', 'Pluto', 'Potomac', 'Prairie Falcon', 'Prescott', 'Presler', 'Prestonia', 'Propus', 'Rana', 'Raphael', 'Raptor Lake-H', 'Raptor Lake-HX', 'Raptor Lake-P', 'Raptor Lake-PS', 'Raptor Lake-R', 'Raptor Lake-S', 'Raptor Lake-U', 'Raven Ridge', 'Raven Ridge 2', 'Regor', 'Rembrandt', 'Rembrandt-R', 'Renoir', 'Richland', 'Rocket Lake', 'Rocket Lake-E', 'Rocket Lake-S', 'Roma', 'Rome', 'Samuel 2']
    #cpu_code_name = ['San Diego', 'Sandy Bridge', 'Sandy Bridge-E', 'Sandy Bridge-EN', 'Sandy Bridge-EP', 'Santa Ana', 'Santa Rosa', 'Sapphire Rapids', 'Sapphire Rapids HBM', 'Sargas', 'Seattle', 'Seoul', 'Sharptooth', 'Siena', 'Sierra Forest', 'Silvermont', 'Silverthorne', 'Skylake', 'Skylake-DT', 'Skylake-H', 'Skylake-SP', 'Skylake-W', 'Skylake-X', 'Skylake-Y', 'SledgeHammer', 'Smithfield', 'Sodaville', 'Sonora', 'Sparta', 'Stealey', 'Stellarton', 'Steppe Eagle', 'Stoney Ridge', 'Storm Peak', 'Strix Point', 'Tanner', 'Temash', 'Thoroughbred', 'Thorton', 'Thuban', 'Thunderbird', 'Thunderbird B', 'Thunderbird C', 'Tiger Lake-H', 'Tiger Lake-U', 'Timna', 'Toledo', 'Toliman', 'Trinity']
    cpu_code_name = ['Troy', 'Tualatin', 'Tulsa', 'Tunnel Creek', 'Valencia', 'Van Gogh', 'Venice', 'Venus', 'Vermeer', 'Vishera', 'Warsaw', 'Westmere-EP', 'Westmere-EX', 'Whiskey Lake-U', 'Willamette', 'Winchester', 'Windsor', 'Wolfdale', 'Woodcrest', 'Yonah', 'Yorkfield', 'ZX-C+', 'Zacate', 'Zambezi', 'Zen', 'Zosma', 'Zurich']

    cpu_specs = []
    current = 1
    f = open("cpu_specs"+current+".txt", "w")
    async with aiohttp.ClientSession() as session:
        for cpu in cpu_code_name:
            site = cpu_site_crawl + cpu
            html, status = await fetch(session, site)
            if status == 200:
                cpu_specs = await parse_cpu_specs(html)
                f.write(cpu_specs.__str__())
                f.write("\n")
                print("finished: ", cpu)
            else:
                while status != 200:
                    time.sleep(30)
                    html, status = await fetch(session, site)
                    if status == 200:
                        await parse_cpu_specs(html)
                        f.write(cpu_specs.__str__())
                        f.write("\n")
                        break
    
def main():
    # asyncio.run(crawl())
    data = [['Name', 'Codename', 'Cores', 'Clock', 'Socket', 'Process', 'L3 Cache', 'TDP', 'Released']]
    for nbfile in range(1, 7):
        with open("cpu_specs"+str(nbfile)+".txt") as f:
            while line := f.readline():
                l = ast.literal_eval(line)
                for cpu in l[2:]:
                    data.append(cpu)
    # with open('cpu_specs.json', 'w') as f:
    #     json.dump(data, f)
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_json('cpu_specs.json', orient='records')
if __name__ == '__main__':
    main()