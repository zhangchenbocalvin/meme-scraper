import requests
import csv
import time
from bs4 import BeautifulSoup as soup

url = "https://old.reddit.com/r/datascience/"
# Headers to mimic a browser visit
headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object
page = requests.get(url, headers=headers)

soup_page = soup(page.text, 'html.parser')

attrs = {'class': 'thing', 'data-domain': 'self.datascience'}
posts = soup_page.find_all('div', attrs=attrs)

counter = 1

while (counter <= 100):
    for post in posts:
        # print(post.attrs['data-domain'])
        title = post.find('p', class_="title").text
        author = post.find('a', class_='author').text
        comments = post.find('a', class_='comments').text
        if comments == "comment":
            comments = 0

        likes = post.find("div", attrs={"class": "score likes"}).text
        if likes == "•":
            likes = "None"

        post_line = [counter, title, author, likes, comments]
        with open('output.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(post_line)

        counter += 1

    next_button = soup_page.find("span", class_="next-button")
    next_page_link = next_button.find("a").attrs['href']
    time.sleep(2)
    page = requests.get(next_page_link, headers=headers)
    soup_page = soup(page.text, 'html.parser')