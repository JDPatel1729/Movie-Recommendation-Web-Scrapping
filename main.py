from bs4 import BeautifulSoup
import requests
import csv

genres = ["fantasy", "drama", "comedy", "adventure",
          "action", "family", "horror",
          "romance", "thriller", "animation",
          "mystery", "musical", "crime",
          "history", "music", "war",
          "western", "biography", "sport"]

print("Available Genres:")

for i in range(len(genres)):
    print(f"{i}. {genres[i].capitalize()}")

genre = int(input("Enter index:"))

print(f"Fetching details for {genres[genre].capitalize()}")

movie_list = []

record_fields = ["Movie Name", "Year", "User Rating"]

name = genres[genre].capitalize()
filename = f"{name}Recommendations.csv"


def fetch():
    content = requests.get(
        f"https://www.imdb.com/search/title/?title_type=feature&genres={name}&view=simple&sort=user_rating,desc&explore=genres"
    ).text

    soup = BeautifulSoup(content, "lxml")

    collection = soup.find_all(
        "div", class_="lister-col-wrapper")

    for index in collection:
        movie_name = index.find('a').text
        year = index.find(
            'span', class_="lister-item-year text-muted unbold").text.replace('(', '').replace(")", "")
        user_rating = index.find(
            'div', class_="col-imdb-rating").strong.text.replace("\n", "").replace(" ", "")
        movie_list.append([movie_name, year, user_rating])

    with open(filename, mode='w') as csv_file:
        # Writer Object
        csv_writer = csv.writer(csv_file)

        # Header Entry
        csv_writer.writerow(record_fields)

        # Record Entry
        csv_writer.writerows(movie_list)


if __name__ == "__main__":
    fetch()
    print(f"Successfully created {filename}")
