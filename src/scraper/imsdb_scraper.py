import requests
from bs4 import BeautifulSoup
import os
import sys
import csv
from urllib import request
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import RAW_IMSDB_MOV_FILE_PATH, IMSDB_URL


def get_imsdb_movies(file_path: str) -> None:
    """
    Scrapes the IMSDB website to get a list of movies and their links.
    """
    url = f"{IMSDB_URL}/all-scripts.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = []
    for movie in tqdm(soup.find_all("p")):
        link = movie.find("a")
        if link:
            movies.append(
                {
                    "title": link.get("title"),
                    "link": IMSDB_URL + link.get("href").replace(" ", "%20"),
                }
            )

    # save the scraped data to a CSV file
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link"])
        writer.writeheader()
        writer.writerows(movies)


def fetch_script_link(movie):
    """
    Fetches the script link for a given movie.
    """
    url = movie["link"].replace(" ", "%20")
    title = movie["title"].replace("\t", " ")
    title = title.replace("Script", "")

    html = request.urlopen(url).read().decode("utf8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    links_in_page = soup.find_all("a")
    found = False
    for link in links_in_page:
        text = link.get_text()
        if "Read" in text and "Script" in text:
            found = True
            script_link = IMSDB_URL + link.get("href")
            movie["script_link"] = script_link
            break
    if not found:
        print("Script not found for ", title)
        movie["script_link"] = None
    return movie


def get_script_links(file_path: str) -> None:
    """
    Fetches the script links for the movies in the input CSV file.
    """
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    # Use ThreadPoolExecutor to fetch script links in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_script_link, movie): movie for movie in data}
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing Script Links"
        ):
            movie = futures[future]
            try:
                result = future.result()
                movie.update(result)
            except Exception as exc:
                print(f"Error processing {movie['title']}: {exc}")

    # Filter out movies without a script link
    data = [movie for movie in data if movie.get("script_link") is not None]

    # write data to a CSV file
    with open(file_path, "w", newline="") as csvfile:
        fieldnames = ["title", "link", "script_link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for movie in data:
            writer.writerow(movie)


if __name__ == "__main__":
    get_imsdb_movies(RAW_IMSDB_MOV_FILE_PATH)
    get_script_links(RAW_IMSDB_MOV_FILE_PATH)
