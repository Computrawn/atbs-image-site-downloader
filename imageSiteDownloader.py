#! python3
# imageSireDownloader.py — An exercise in web scraping.
# For more information, see project_detail.txt.

import concurrent.futures
import requests
import bs4

img_list = []
unsplash_name = []


def find_source(search_object):
    """Extract image source links using beautiful soup."""
    res = requests.get(search_object, timeout=60.0)
    res.raise_for_status()
    soup_file = bs4.BeautifulSoup(res.text, "lxml")
    image_container = soup_file.find_all(class_="MorZF")
    for image in image_container:
        img_list.append(image.img["src"])


def filter_links(img_list):
    """Further filters source links to isolate urls and filenames."""
    for img in img_list:
        img_id = img.split("/")[3]
        img_match = img_id[:5]
        if img_match == "photo":
            img_name = img_id.split("?")
            file_name = img_name[0]
            unsplash_name.append(file_name)


def link_downloader(unsplash):
    for name in unsplash:
        unsplash_link = f"https://images.unsplash.com/{name}"
        unsplash_filename = f"{name}.jpg"
        img_bytes = requests.get(unsplash_link, timeout=60.0).content
        with open(unsplash_filename, "wb") as image_file:
            image_file.write(img_bytes)
            print(f"Downloading {unsplash_link} as {unsplash_filename}.")


user_input = input("What would you like to search for? ")
url = f"https://unsplash.com/s/photos/{user_input}"

find_source(url)
filter_links(img_list)
link_downloader(unsplash_name)
