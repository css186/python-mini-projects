"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

This program consists a class that will generate all the elements necessary in the breakout game.
import this file and the class to instantiate instance.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.graphics.gimage import GImage

import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create screen variable
        self.__screen = 0

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle and filled its color with black
        self.paddle = GRect(paddle_width, paddle_height, x=(window_width-paddle_width)/2, y=window_height-paddle_offset)
        self.paddle.filled = True
        self.paddle.fill_color = "Black"
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2, x=(window_width-ball_radius)/2, y=(window_height-ball_radius)/2)
        self.ball.filled = True
        self.ball.fill_color = "Black"
        self.window.add(self.ball)

        # Default initial velocity for the ball
        # set strong private instance variable for velocity of the ball(default zero)
        self.__dx, self.__dy = 0, 0
        self._initialize_ball_velo()

        # set a variable to determine ball's activation
        self.is_ball_activated = False

        # Initialize our mouse listeners
        onmouseclicked(self._mouse_click)
        onmousemoved(self._mouse_move)

        # create brick-related variables
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_offset = brick_offset
        self.brick_spacing = brick_spacing

        # Draw bricks
        self._create_bricks(brick_rows, brick_cols, brick_width, brick_height, brick_offset, brick_spacing)

        # create scoreboard
        self.score_board = GLabel("Score: 0")
        self.score_board.font = "San Francisco-20"
        self.score_board.color = "black"
        self.window.add(self.score_board, 10, self.window.height - 5)

        # create hp bar
        self.hp_list = list()
        for idx, self._hp in enumerate(range(3)):
            self._hp = GImage("img/hp.png")
            self.window.add(self._hp,
                            self.window.width - (idx + 1) * 25,
                            self.window.height - 25)
            self.hp_list.append(self._hp)

        # create game_over page related variable
        self.game_over_label = None

    def update_score(self, count):
        score = count * 10
        self.score_board.text = f"Score: {score}"

    def _create_bricks(self, rows, columns, width, height, offset, spacing):
        """
        a private method to create all the bricks
        @param rows: number of rows of bricks
        @param columns: number of columns of bricks
        @param width: width of a brick
        @param height: height of a brick
        @param offset: vertical offset of the topmost brick from the window top (in pixels)
        @param spacing: space between each brick (in pixels)
        @return: None
        """
        # create color list
        colors = ["red", "orange", "yellow", "green", "blue"]

        # create color index
        index = 0

        for row in range(rows):
            if row % 2 == 0 and row != 0:
                index += 1
            for column in range(columns):
                self.brick = GRect(width, height)
                self.brick.filled = True
                self.brick.fill_color = colors[index]
                self.brick.color = colors[index]
                self.window.add(self.brick, x=column*(self.brick.width+spacing),
                                y=offset + row*(self.brick.height+spacing))

    def _mouse_click(self, mouse):
        """
        a private method to control the mouse click
        @param mouse: mouse listener
        @return: None
        """
        if self.screen != 1 or self.screen != 2:
            self.is_ball_activated = True
        else:
            self.is_ball_activated = False

    def _mouse_move(self, mouse):
        """
        a private method to control the movement of mouse
        @param mouse: mouse listener
        @return: none
        """
        # horizontal movement only
        self.paddle.x = mouse.x - self.paddle.width / 2

        # when paddle touch the boundary of window
        if self.paddle.x <= 0:
            self.paddle.x = 0
        elif self.paddle.x + self.paddle.width >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width

    # define dx getter and setter
    @property
    def dx(self):
        return self.__dx

    @dx.setter
    def dx(self, dx):
        self.__dx = dx

    # define dy getter and setter
    @property
    def dy(self):
        return self.__dy

    @dy.setter
    def dy(self, dy):
        self.__dy = dy

    # define screen getter and setter
    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, screen):
        self.__screen = screen

    def _initialize_ball_velo(self):
        """
        a private method to predefine ball's velocity
        @return: None
        """
        # set default __dy
        # set default __dy
        self.dy = INITIAL_Y_SPEED

        # set default __dx
        self.dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.dx = -self.dx

    def reset_ball_velo(self):
        if random.random() > 0.5:
            self.dx = -self.dx

    def reset_ball_location(self):
        """
        a method to reset ball to its starting position
        @return: None
        """
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.width) / 2

    def game_over_page(self):
        self.window.clear()
        self.game_over_label = GLabel("Game Over")
        self.game_over_label.font = "San Francisco-50"
        self.game_over_label.color = "Black"
        self.window.add(self.game_over_label,
                        (self.window.width - self.game_over_label.width)/2,
                        (self.window.height + self.game_over_label.height)/2)
        self.score_board = GLabel("Score: 0")
        self.window.add(self.score_board)
        self.screen = 1

    def winning_page(self):
        self.window.clear()
        self.game_over_label = GLabel("You Win!")
        self.game_over_label.font = "San Francisco-50"
        self.game_over_label.color = "Black"
        self.window.add(self.game_over_label,
                        (self.window.width - self.game_over_label.width)/2,
                        (self.window.height + self.game_over_label.height)/2)

        self.screen = 2







