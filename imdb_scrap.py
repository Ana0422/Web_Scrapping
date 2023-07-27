import json
from bs4 import BeautifulSoup
import urllib.request
import requests
import pandas as pd
import time

# Define a custom user-agent header to mimic a legitimate browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_movie_ids(num=30, page=1):
    links_data = pd.read_csv("links.csv")
    movie_ids = list(links_data.imdbId)
    start_index = (page - 1) * num
    end_index = start_index + num
    return movie_ids[start_index:end_index]


def scrape_index_page(movie_id):
    movie_index_url = "https://www.imdb.com/title/tt{}/".format(
        str(movie_id).zfill(7))
    try:
        current_page = requests.get(movie_index_url, headers=HEADERS)
        current_page.raise_for_status()  # Check if the request was successful
        index_soup = BeautifulSoup(current_page.text, "html.parser")
        current_page_json = index_soup.find(
            "script", attrs={"type": "application/ld+json"})
        if current_page_json:
            current_page_json = str(current_page_json)[
                str(current_page_json).find('{'):-9]
            return current_page_json
        else:
            print(f"JSON data not found for movie_id: {movie_id}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for movie_id: {movie_id}. Exception: {e}")
        return None


def collect_movie_dict(movie_id):
    page_json = json.loads(scrape_index_page(movie_id))
    if page_json:
        movie = {
            "name": page_json.get("name", ""),
            "genre": page_json.get("genre", ""),
            "image": page_json.get("image", ""),
            "description": page_json.get("description", ""),
        }
        print(movie["name"])
        return movie
    else:
        return None


def get_movies_paged(page=1, movies_per_page=20):
    ids = get_movie_ids(num=movies_per_page, page=page)
    scrape_result = {"movies": []}
    for movie_id in ids:
        movie_data = collect_movie_dict(movie_id)
        if movie_data:
            scrape_result["movies"].append(movie_data)
        # Introduce a delay of 2 seconds between each request to avoid overwhelming the server
        time.sleep(2)
    return scrape_result


if __name__ == "__main__":
    ids = get_movie_ids(10)
    print(ids)
    for movie_id in ids:
        collect_movie_dict(movie_id)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_movie_ids(num=30, page=1):
    links_data = pd.read_csv("links.csv")
    movie_ids = list(links_data.imdbId)
    start_index = (page - 1) * num
    end_index = start_index + num
    return movie_ids[start_index:end_index]


def scrape_index_page(movie_id):
    movie_index_url = "https://www.imdb.com/title/tt{}/".format(
        str(movie_id).zfill(7))
    try:
        current_page = requests.get(movie_index_url, headers=HEADERS)
        current_page.raise_for_status()
        index_soup = BeautifulSoup(current_page.text, "html.parser")
        current_page_json = index_soup.find(
            "script", attrs={"type": "application/ld+json"})
        if current_page_json:
            current_page_json = str(current_page_json)[
                str(current_page_json).find('{'):-9]
            return current_page_json
        else:
            print(f"JSON data not found for movie_id: {movie_id}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for movie_id: {movie_id}. Exception: {e}")
        return None


def collect_movie_dict(movie_id):
    page_json = json.loads(scrape_index_page(movie_id))
    if page_json:
        movie = {
            "name": page_json.get("name", ""),
            "genre": page_json.get("genre", ""),
            "image": page_json.get("image", ""),
            "description": page_json.get("description", ""),
        }
        print(movie["name"])
        return movie
    else:
        return None


def get_movies_paged(page=1, movies_per_page=20):
    ids = get_movie_ids(num=movies_per_page, page=page)
    scrape_result = {"movies": []}
    for movie_id in ids:
        movie_data = collect_movie_dict(movie_id)
        if movie_data:
            scrape_result["movies"].append(movie_data)
        time.sleep(2)

    return scrape_result


if __name__ == "__main__":
    ids = get_movie_ids(10)
    print(ids)
    for id in ids:
        collect_movie_dict(movie_id)
