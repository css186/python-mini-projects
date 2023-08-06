"""
File: babynames.py
Name: Brian Chen
--------------------------
SC101 Baby Names Project
Adapted from Nick Parlante"s Baby Names assignment by
Jerry Liao.
"""

import sys


def add_data_for_name(name_data: dict, year: str, rank: str, name: str) -> None:
    """
    Adds the given year and rank to the associated name in the name_data dict.

    Input:
        name_data (dict): dict holding baby name data
        year (str): the year of the data entry to add
        rank (str): the rank of the data entry to add
        name (str): the name of the data entry to add

    Output:
        This function modifies the name_data dict to store the provided
        name, year, and rank. This function does not return any value.
    """
    # check if name is not in name_data, if true then append {year: rank}
    if name not in name_data:
        name_data[name] = {year: rank}

    # check if year is not in sub_dict, if true then append rank
    if year not in name_data[name]:
        name_data[name][year] = rank
    else:
        if int(rank) < int(name_data[name][year]):
            name_data[name][year] = rank


def add_file(name_data: dict, filename: str) -> None:
    """
    Reads the information from the specified file and populates the name_data
    dict with the data found in the file.

    Input:
        name_data (dict): dict holding baby name data
        filename (str): name of the file holding baby name data

    Output:
        This function modifies the name_data dict to store information from
        the provided file name. This function does not return any value.
    """
    # open file
    with open(filename, "r") as f:
        # read in all the lines
        lines = f.readlines()
        # set first line as year variable
        year = lines[0].strip()

        # read other lines and store each corresponding variables
        for data in lines[1:]:
            data = data.strip().split(",")  # data will become a list
            # strip space and store in variables
            rank = data[0].strip()
            male_name = data[1].strip()
            female_name = data[2].strip()

            add_data_for_name(name_data, year, rank, male_name)
            add_data_for_name(name_data, year, rank, female_name)


def read_files(filenames: list) -> dict:
    """
    Reads the data from all files specified in the provided list
    into a single name_data dict and then returns that dict.

    Input:
        filenames (List[str]): a list of filenames containing baby name data

    Returns:
        name_data (dict): the dict storing all baby name data in a structured manner
    """
    name_data = {}
    for file in filenames:
        add_file(name_data, file)

    return name_data


def search_names(name_data: dict, target: str) -> list[str]:
    """
    Given a name_data dict that stores baby name information and a target string,
    returns a list of all names in the dict that contain the target string. This
    function should be case-insensitive with respect to the target string.

    Input:
        name_data (dict): a dict containing baby name data organized by name
        target (str): a string to look for in the names contained within name_data

    Returns:
        matching_names (List[str]): a list of all names from name_data that contain
                                    the target string
    """
    matched_names = []

    for name in name_data:
        if target.lower() in name.lower():
            matched_names.append(name)

    return matched_names


def print_names(name_data: dict) -> None:
    """
    (provided, DO NOT MODIFY)
    Given a name_data dict, print out all its data, one name per line.
    The names are printed in alphabetical order,
    with the corresponding years data displayed in increasing order.

    Input:
        name_data (dict): a dict containing baby name data organized by name
    Returns:
        This function does not return anything
    """
    for key, value in sorted(name_data.items()):
        print(key, sorted(value.items()))


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # Two command line forms
    # 1. file1 file2 file3 ..
    # 2. -search target file1 file2 file3 ..

    # Assume no search, so list of filenames to read
    # is the args list
    filenames = args

    # Check if we are doing search, set target variable
    target = ""
    if len(args) >= 2 and args[0] == "-search":
        target = args[1]
        filenames = args[2:]  # Update filenames to skip first 2

    # Read in all the filenames: baby-1990.txt, baby-2000.txt, ...
    names = read_files(filenames)

    # Either we do a search or just print everything.
    if len(target) > 0:
        search_results = search_names(names, target)
        for name in search_results:
            print(name)
    else:
        print_names(names)


if __name__ == "__main__":
    main()
