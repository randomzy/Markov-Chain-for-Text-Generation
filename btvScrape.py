import os
import requests
import time
from bs4 import BeautifulSoup

page_id = 2036
url1 = f"https://btvnovinite.bg/bulgaria/?page={page_id}"
url2 = f"https://btvnovinite.bg/svetut/?page={page_id}"

with open('news_world.txt', 'a') as file:
    page = requests.get(url2)
    soup = BeautifulSoup(page.content, 'html.parser')
    while(titles := soup.find_all("div", class_="title")):
        print(page_id)
        for title in titles:
            title_txt = title.find(text=True)
            title_txt = title_txt + '.\n'   
            file.writelines(title_txt)
        page_id = page_id + 1
        url2 = f"https://btvnovinite.bg/svetut/?page={page_id}"
        page = requests.get(url2)
        soup = BeautifulSoup(page.content, 'html.parser')
        time.sleep(0.5)