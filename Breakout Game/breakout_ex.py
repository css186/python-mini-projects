"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This file will display the game while being executed
"""
import random

from campy.gui.events.timer import pause
from breakoutgraphics_ex import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
num_lives = 3		    # Number of attempts

# create brick count variable
brick_count = 0


def main():
    """
    Generate all the elements in the game and the logic of ball movement behind
    @return: None
    """
    global num_lives, brick_count

    graphics = BreakoutGraphics()

    game_playing = True

    dead_ball = False

    while True:

        # if game over or win, break
        if not game_playing:
            break

        # create horizontal movement variable
        move_h = graphics.dx

        # create vertical movement variable
        move_v = graphics.dy

        # create unbreakable item list
        # add score board first
        unbreakable = [graphics.score_board]
        # loop in lives_list and add all element inside to unbreakable list
        for hp in graphics.hp_list:
            unbreakable.append(hp)

        # Add the animation loop here!
        while True:

            # check remaining bricks
            if brick_count == (graphics.brick_rows * graphics.brick_cols):
                # if break count equals total brick count, then win the game
                graphics.winning_page()
                game_playing = False
                break

            # check remaining hp
            if num_lives == 0:
                graphics.game_over_page()
                game_playing = False
                break

            # check ball's activation, if ball is activated then move the ball
            if num_lives > 0:
                if graphics.is_ball_activated:
                    graphics.ball.move(move_h, move_v)

                # check collision with bricks or paddle
                # only consider ball came from the top as a valid collision, so add condition of move_v > 0
                if move_v > 0:
                    bottom_left = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y + graphics.ball.height)
                    bottom_right = graphics.window.get_object_at(graphics.ball.x + graphics.ball.width, graphics.ball.y + graphics.ball.height)

                    if bottom_left is graphics.paddle or bottom_right is graphics.paddle:
                        # change vertical direction
                        move_v *= -1

                    # enable bouncing between bricks
                    elif bottom_left is not None and bottom_left is not graphics.paddle \
                            and bottom_left not in unbreakable:
                        graphics.window.remove(bottom_left)
                        # count brick
                        brick_count += 1
                        # change direction
                        move_v *= -1

                    elif bottom_right is not None and bottom_right is not graphics.paddle \
                            and bottom_right not in unbreakable:
                        # remove bricks
                        graphics.window.remove(bottom_right)
                        # count brick
                        brick_count += 1
                        # change direction
                        move_v *= -1

                else:
                    upper_left = graphics.window.get_object_at(graphics.ball.x, graphics.ball.y)
                    upper_right = graphics.window.get_object_at(graphics.ball.x + graphics.ball.width, graphics.ball.y)

                    if upper_left is not None and upper_left is not graphics.paddle:
                        # remove bricks
                        graphics.window.remove(upper_left)
                        # count brick
                        brick_count += 1

                        # update score
                        graphics.update_score(brick_count)

                        # change direction
                        move_v *= -1

                    elif upper_right is not None and upper_right is not graphics.paddle:
                        # remove bricks
                        graphics.window.remove(upper_right)
                        # count brick
                        brick_count += 1

                        # update score
                        graphics.update_score(brick_count)

                        # change direction
                        move_v *= -1

                    elif upper_right is graphics.paddle or upper_right is graphics.paddle:
                        move_v *= -1

                # check collision with boundaries:
                # if ball touches left or right boundary, ball ricochets
                if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                    # change horizontal direction
                    move_h *= -1

                # if ball touches top boundary, ball ricochets
                if graphics.ball.y <= 0:
                    # change vertical direction
                    move_v *= -1

                if graphics.ball.y + graphics.ball.height >= graphics.window.height:
                    graphics.reset_ball_location()
                    graphics.is_ball_activated = False
                    num_lives -= 1
                    dead_ball = True
                    # pop hp from head
                    graphics.window.remove(graphics.hp_list.pop())

            pause(FRAME_RATE)


if __name__ == '__main__':
    main()
