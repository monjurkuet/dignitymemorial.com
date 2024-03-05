import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
headers = {
    'authority': 'www.dignitymemorial.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


start=0
request_url='https://www.dignitymemorial.com/en//obituaries/ObituariesSearch/More?varQuery=q%3D(and%20(and%20%27%27)%20(or%20locationstate%3A%27CA%27)%20(or%20cmicreationdate%3A%5B%272024-02-20T00%3A00%3A00Z%27%2C%7D)%20%20%20)%26start%3D{}%26size%3D20%26filtergroup%3Dcmicreationdate%26filtervalue%3Dnull%26filterchecked%3Dfalse%26grave%3Dfalse&grave=false'

final_data=[]

while True:
    response = requests.get(request_url.format(start)
        ,
        headers=headers,
    )
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all elements with the class "obit-result-container"
    obit_containers = soup.find_all('div', class_='obit-result-container')
    for each_line in obit_containers:
        obit_text = each_line.find_all('p')[-1].text.strip()
        split_text=obit_text.split(',')
        name=split_text[0]
        Age=split_text[1].split(' ')[-1]
        city=split_text[2].split('of')[-1].strip()+', '+split_text[3].split('passed')[0].strip()
        updatedAt=datetime.now()
        data={'name':name,'Age':Age,'city':city,'updatedAt':updatedAt}
        final_data.append(data)
        print(data)
    start+=10
    time.sleep(random.uniform(2,5))