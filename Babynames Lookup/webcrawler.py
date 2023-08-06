"""
File: webcrawler.py
Name: Brian Chen
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10900879
Female Number: 7946050
---------------------------
2000s
Male Number: 12977993
Female Number: 9209211
---------------------------
1990s
Male Number: 14146310
Female Number: 10644506
"""
import string

import requests
from bs4 import BeautifulSoup
import time


def main() -> None:
    """
    this method will print out the number of top200 male and female in 1990s, 2000s, and 2010s from ssa.gov on Console
    each loop time will also be calculated
    @return: None
    """

    for year in ["2010s", "2000s", "1990s"]:

        # set start time for each outer loop
        start_time = time.time()

        print("---------------------------")
        print(year)
        url = "https://www.ssa.gov/oact/babynames/decades/names"+year+".html"
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # search for tbody tag, select all tags start with "tr", drop last element in the list
        # then store in contents variable
        contents = soup.tbody.select("tr")[:-1]

        # initialize male_total and female_total variable
        male_total = 0
        female_total = 0

        # iterate contents and select text within "td" tags
        for content in contents:
            table_data = content.select("td")  # return a list

            # remove punctuation
            male_count = table_data[2].text.translate(str.maketrans("", "", string.punctuation))
            female_count = table_data[4].text.translate(str.maketrans("", "", string.punctuation))

            male_total += int(male_count)
            female_total += int(female_count)

        print(f"Male Number: {male_total}")
        print(f"Female Number: {female_total}")

        # set end time for each outer loop
        end_time = time.time()

        # calculate loop time
        execution_time = end_time - start_time
        print(f"Execution Time: {execution_time:.4f} seconds")


if __name__ == "__main__":
    main()
