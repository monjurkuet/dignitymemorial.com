import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import pandas as pd
from datetime import datetime

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
retrycounter=0

print("Scraping obituaries...")


while True and retrycounter<20:
    response = requests.get(request_url.format(start)
        ,
        headers=headers,
    )
    if response.status_code!=200:
        retrycounter-=1
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all elements with the class "obit-result-container"
        obit_containers = soup.find_all('div', class_='obit-result-container')
        if not obit_containers:
            retrycounter+=1
        else:
            for each_line in obit_containers:
                try:
                    obit_text = each_line.find_all('p')[-1].text.strip()
                    split_text=obit_text.split(',')
                    name=split_text[0]
                    if 'años' in each_line.text:
                        Age=split_text[1].split(' ')[1]
                        city=None
                    else:
                        Age=split_text[1].split('age')[1].split(' ')[1]
                    if ', of' in each_line.text:
                        #city=split_text[2].split('of')[-1].strip()+', '+split_text[3].split('passed')[0].strip()
                        city=split_text[2].split('of')[-1].strip()
                    else:
                        city=None
                    updatedAt=datetime.now()
                    data={'name':name,'Age':int(Age),'city':city,'updatedAt':updatedAt}
                    final_data.append(data)
                    print(f"Scraped: {data}")
                except:
                    pass
        start+=10
    time.sleep(random.uniform(2,5))

# Modify the filename to include today's date
today_date_str = datetime.now().strftime("%Y%m%d")
output_file = f'data_{today_date_str}.xlsx'

df = pd.DataFrame.from_dict(final_data)
# Save the DataFrame to the Excel file with today's date in the filename
try:
    # Save the DataFrame to the Excel file with today's date in the filename
    df.to_excel(output_file, index=False)
    print(f'Data saved to {output_file}')
except Exception as e:
    print(f"Error saving data to Excel file: {e}")