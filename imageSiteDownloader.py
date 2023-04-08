#! python3
# imageSireDownloader.py — An exercise in web scraping.
# For more information, see project_detail.txt.
import re
import requests
import bs4

img_list = []


def photo_downloader(search_object):
    res = requests.get(search_object, timeout=60.0)
    res.raise_for_status()
    soup_file = bs4.BeautifulSoup(res.text, "lxml")
    image_container = soup_file.find_all(class_="MorZF")
    for image in image_container:
        img_class = image.find_all("img")
        img_list.append(img_class)


def print_list(img_list):
    for img in img_list:
        print(img)
        print("<-----*****----->")


user_input = input("What would you like to search for? ")
url = f"https://unsplash.com/s/photos/{user_input}"

photo_downloader(url)
print_list(img_list)
