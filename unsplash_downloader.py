#! python3
# unsplash_downloader.py — An exercise in web scraping.
# For more information, see project_detail.txt.

import concurrent.futures
import requests
from bs4 import BeautifulSoup


def find_source(search_object):
    """Extract image source links using beautiful soup."""
    res = requests.get(search_object, timeout=60.0)
    res.raise_for_status()
    soup_file = BeautifulSoup(res.text, "lxml")
    image_container = soup_file.find_all(class_="MorZF")
    img_list = [image.img["src"] for image in image_container]
    return img_list


def filter_links(img_list):
    """Filters source links to isolate urls and filenames."""
    unsplash_name = [
        img.split("/")[3].split("?")[0]
        for img in img_list
        if img.split("/")[3][:5] == "photo"
    ]
    return unsplash_name


def downloader(unsplash):
    """Downloads files from list."""
    unsplash_link = f"https://images.unsplash.com/{unsplash}"
    img_bytes = requests.get(unsplash_link, timeout=60.0).content
    with open(f"photos/{unsplash}.jpg", "wb") as image_file:
        image_file.write(img_bytes)


def main():
    image_links = find_source(
        f"https://unsplash.com/s/photos/{input('What would you like to search for? ')}"
    )
    unsplash_name = filter_links(image_links)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(downloader, unsplash_name)


if __name__ == "__main__":
    main()
