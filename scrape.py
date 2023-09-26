import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

response = requests.get("https://www.youtube.com/results?search_query=just+a+lil+bit+murdbrain+level+8+flyn+stoned", headers=headers) 
# print(response.text)

# file = open('response.txt', 'w')
# file.write(response.text)
# file.close()

# TODO:
# https://pypi.org/project/requests-html/#description Check here next to see if u can scrape JS
with open('response.txt', "w", encoding="utf-8") as f:
    f.write(response.text)
soup = BeautifulSoup(response.text, "html.parser")

print("\n\n" + soup.prettify() + "\n\n\n")





