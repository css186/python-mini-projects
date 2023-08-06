"""
File: babygraphics.py
Name: Brian Chen
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante"s Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    "data/full/baby-1900.txt", "data/full/baby-1910.txt",
    "data/full/baby-1920.txt", "data/full/baby-1930.txt",
    "data/full/baby-1940.txt", "data/full/baby-1950.txt",
    "data/full/baby-1960.txt", "data/full/baby-1970.txt",
    "data/full/baby-1980.txt", "data/full/baby-1990.txt",
    "data/full/baby-2000.txt", "data/full/baby-2010.txt"
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ["red", "purple", "green", "blue"]
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width: int, year_index: int) -> int:
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    return GRAPH_MARGIN_SIZE + year_index * ((width - GRAPH_MARGIN_SIZE * 2) // len(YEARS))


def get_y_coordinate(height: int, rank: str) -> int:
    """
    Given the height of the canvas and the rank of the current year
    returns the y coordinate where the rank should be drawn.

    Input:
        height (int): The height of the canvas
        rank (str): The rank number
    Returns:
        y_coordinate (int): The y coordinate of the rank.
    """
    return GRAPH_MARGIN_SIZE + int(rank) * (height - GRAPH_MARGIN_SIZE * 2) // MAX_RANK


def draw_fixed_lines(canvas: tkinter):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete("all")            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    # draw horizontal lines on canvas
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       width=LINE_WIDTH, fill="black")
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, width=LINE_WIDTH, fill="black")

    # draw straight lines and year text labels on canvas
    for index in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, index), 0, get_x_coordinate(CANVAS_WIDTH, index),
                           CANVAS_HEIGHT, width=LINE_WIDTH, fill="black")
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, index) + TEXT_DX, CANVAS_HEIGHT, text=str(YEARS[index]),
                           anchor=tkinter.SW, fill="black")


def draw_names(canvas: tkinter, name_data: dict, lookup_names: list[str]) -> None:
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #

    # initialize color_index variable
    color_index = 0

    # traverse all searched names
    for name in lookup_names:
        # store each year position in a list
        positions = []

        # loop thru name_data to get name
        if name in name_data:
            # get index and year for each element in YEARS
            for index, year in enumerate(YEARS):
                if str(year) in name_data[name]:
                    # store coordinate into tuple
                    positions.append((index, name_data[name][str(year)]))
                else:
                    positions.append((index, "*"))

            # get colors based on the remainder as index
            color = COLORS[color_index % len(COLORS)]
            draw_names_line(canvas, name, positions, color)
            color_index += 1


def draw_names_line(canvas: tkinter, name: str, positions: list, color: str) -> None:

    for i in range(0, len(positions) - 1):
        previous_x = get_x_coordinate(CANVAS_WIDTH, positions[i][0])
        previous_y = get_y_coordinate(CANVAS_HEIGHT, positions[i][1]) if positions[i][1] != "*" \
            else CANVAS_HEIGHT - GRAPH_MARGIN_SIZE

        current_x = get_x_coordinate(CANVAS_WIDTH, positions[i + 1][0])
        current_y = get_y_coordinate(CANVAS_HEIGHT, positions[i + 1][1]) if positions[i + 1][1] != "*" \
            else CANVAS_HEIGHT - GRAPH_MARGIN_SIZE

        canvas.create_line(previous_x, previous_y, current_x, current_y, width=LINE_WIDTH, fill=color)

        last_text = name + " *" if positions[i][1] == "*" else name + " " + positions[i][1]
        now_text = name + " *" if positions[i + 1][1] == "*" else name + " " + positions[i + 1][1]

        canvas.create_text(previous_x, previous_y, text=last_text, anchor=tkinter.SW, fill=color)
        canvas.create_text(current_x, current_y, text=now_text, anchor=tkinter.SW, fill=color)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title("Baby Names")
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == "__main__":
    main()
