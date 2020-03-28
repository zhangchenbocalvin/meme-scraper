import requests
from bs4 import BeautifulSoup as soup
from random import randint

def get_image():
  print("*** SCRAPING ***")
  print()
  url = "https://old.reddit.com/r/Coronavirus_Meme/"
  # Headers to mimic a browser visit
  headers = {'User-Agent': 'Mozilla/5.0'}

  # Returns a requests.models.Response object
  page = requests.get(url, headers=headers)

  soup_page = soup(page.text, 'html.parser')

  attrs = {'class': 'thing', 'data-domain': 'i.redd.it'}

  counter = 0
  page_number = 0

  images = []
  messages = []

  while (True):
    print("** Page " + str(page_number) + " **")
    print()
    posts = soup_page.find_all('div', attrs=attrs)
    for post in posts:
      print("* Post " + str(counter) + " *")
      # gets the link for the image
      thumbnail = post.find("a", class_="thumbnail")
      thumbnail_page_link = 'http://old.reddit.com' + thumbnail.attrs['href'] + '?'
      image_page = requests.get(thumbnail_page_link, headers=headers)
      image_soup_page = soup(image_page.text, 'html.parser')
      file = image_soup_page.find("img", class_="preview")
      file_link = file.attrs['src']
      images.append(file_link)

      # gets the meme message
      entry = post.find("div", class_="entry")
      messages.append(entry.div.p.a.text)

      counter += 1

      if (counter == 10):
        index = randint(0, len(images) - 1)

        return images[index], messages[index]
    
    page_number += 1

    next_button = soup_page.find("span", class_="next-button")
    next_page_link = next_button.find("a").attrs['href']
    page = requests.get(next_page_link, headers=headers)
    soup_page = soup(page.text, 'html.parser')


image, message = get_image()
print("Go to this page for your meme: " + image)
print("This is the message for this meme: " + message)