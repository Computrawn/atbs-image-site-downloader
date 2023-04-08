#! python3
# imageSireDownloader.py — An exercise in web scraping.
# For more information, see project_detail.txt.

import concurrent.futures
import requests
import time
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


def nothread_downloader(unsplash):
    """Downloads files from list."""
    for name in unsplash:
        unsplash_link = f"https://images.unsplash.com/{name}"
        unsplash_filename = f"{name}.jpg"
        img_bytes = requests.get(unsplash_link, timeout=60.0).content
        with open(f"photos/{unsplash_filename}", "wb") as image_file:
            image_file.write(img_bytes)


def thread_downloader(unsplash):
    """Downloads files from list."""
    unsplash_link = f"https://images.unsplash.com/{unsplash}"
    unsplash_filename = f"{unsplash}.jpg"
    img_bytes = requests.get(unsplash_link, timeout=60.0).content
    with open(f"photos/{unsplash_filename}", "wb") as image_file:
        image_file.write(img_bytes)


user_input = input("What would you like to search for? ")
url = f"https://unsplash.com/s/photos/{user_input}"

find_source(url)
filter_links(img_list)

start = time.perf_counter()
# nothread_downloader(
#     unsplash_name
# )  # This is where I'd like to test concurrent futures model to see if I can boost performance with threading.

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(thread_downloader, unsplash_name)

finish = time.perf_counter()
print(f"Downloaded all files in {finish - start} seconds.")
