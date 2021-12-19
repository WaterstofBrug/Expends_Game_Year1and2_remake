import pyglet
from pyglet import shapes
from pyglet.window import key
import copy as c
import math
from pyglet.gl import *

label = 0
point = None


def valid_move(pos, size, size_type, area, offset):
    if size_type == 'radius':
        if pos[0] >= area[0] - offset / 2 - size:
            return False
        elif pos[0] <= offset / 2 + size:
            return False
        elif pos[1] >= area[1] - offset / 2 - size:
            return False
        elif pos[1] <= offset / 2 + size:
            return False
        else:
            return True

    elif size_type == 'quadrilateral':
        if pos[0] >= area[0] - offset / 2 - size + 1:
            return False
        elif pos[0] <= offset / 2:
            return False
        elif pos[1] >= area[1] - offset / 2 - size + 1:
            return False
        elif pos[1] <= offset / 2:
            return False
        else:
            return True


def collision(circ_pos, circ_size, sqr_pos, sqr_size):
    positive_sqr_pos = [0, 0]

    if sqr_pos[0] <= circ_pos[0]-circ_size:
        positive_sqr_pos[0] = abs(sqr_pos[0] - circ_pos[0]) + circ_pos[0] - sqr_size
    else:
        positive_sqr_pos[0] = abs(sqr_pos[0] - circ_pos[0]) + circ_pos[0]

    if sqr_pos[1] <= circ_pos[1]-circ_size:
        positive_sqr_pos[1] = abs(sqr_pos[1] - circ_pos[1]) + circ_pos[1] - sqr_size
    else:
        positive_sqr_pos[1] = abs(sqr_pos[1] - circ_pos[1]) + circ_pos[1]

    if math.sqrt((circ_pos[0] - positive_sqr_pos[0]) ** 2 + (circ_pos[1] - positive_sqr_pos[1]) ** 2) <= circ_size:
        return [True, positive_sqr_pos]
    else:
        return [False, positive_sqr_pos]


def main():
    win_dim = (1000, 800)
    offset = 50
    player_size = 50
    step_size = 20

    class Player:
        def __init__(self, name, type, size, x, y, color):
            self.name = name
            self.type = type
            self.size = size
            self.position = (x, y)
            self.color = color

    logo = pyglet.image.load('images/tag_icon.png')
    window = pyglet.window.Window(width=win_dim[0], height=win_dim[1], caption='Tag')
    window.set_icon(logo)
    batch = pyglet.graphics.Batch()
    text = pyglet.graphics.Batch()
    BG_ = pyglet.graphics.Batch()

    field = shapes.Rectangle(x=offset / 2, y=offset / 2, width=win_dim[0] - offset, height=win_dim[1] - offset,
                             color=(50, 50, 60), batch=BG_)
    background = pyglet.image.load('images/background.png')

    texture = background.get_texture()
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    texture.width = 400  # resize from 8x8 to 16x16
    texture.height = 400
    texture.blit(100, 30)

    sprite = pyglet.sprite.Sprite(img=background, x=win_dim[0]/2-200, y=win_dim[1]/2-200, batch=BG_)

    player1 = Player('P1', 'circle', player_size, 100, 400 - player_size / 2, (255, 70, 70))
    player2 = Player('P2', 'square', player_size * 1.7, 850, 400 - player_size * 1.7, (255, 255, 70))
    score = {player1.name: 0, player2.name: 0}

    circle_shadow = shapes.Circle(x=player1.position[0], y=player1.position[1], radius=player1.size,
                                  color=(70, 70, 80), batch=batch)
    circle_shadow_ = shapes.Circle(x=player1.position[0], y=player1.position[1], radius=player1.size - 10,
                                   color=(50, 50, 60), batch=batch)
    square_shadow = shapes.Rectangle(x=player2.position[0], y=player2.position[1], width=player2.size,
                                     height=player2.size, color=(70, 70, 80), batch=batch)
    square_shadow_ = shapes.Rectangle(x=player2.position[0] + 10, y=player2.position[1] + 10, width=player2.size - 20,
                                      height=player2.size - 20, color=(50, 50, 60), batch=batch)
    circle = shapes.Circle(x=player1.position[0], y=player1.position[1], radius=player1.size, color=player1.color,
                           batch=batch)
    square = shapes.Rectangle(x=player2.position[0], y=player2.position[1], width=player2.size, height=player2.size,
                              color=player2.color, batch=batch)
    global label
    label = pyglet.text.Label(f'SCORE: {score[player1.name]} | {score[player2.name]}',
                              font_name='Super Legend Boy', font_size=20, x=win_dim[0] / 2 - 120, y=win_dim[1] - 50)

    kill1_sound = pyglet.media.load('sounds/kill.wav', streaming=False)
    kill2_sound = pyglet.media.load('sounds/kill2.wav', streaming=False)

    battle_music = pyglet.media.load('sounds/battle_music.wav', streaming=False)
    player = pyglet.media.Player()
    player.queue(battle_music)
    player.play()

    @window.event()
    def on_key_press(symbol, modifiers):
        c_pos_circ = c.copy(circle.position)
        c_pos_sqr = c.copy(square.position)
        global label
        global point

        if symbol == key.W:
            c_pos_circ = (circle.position[0], circle.position[1] + step_size)
            moving = player1.name
        elif symbol == key.S:
            c_pos_circ = (circle.position[0], circle.position[1] - step_size)
            moving = player1.name
        elif symbol == key.A:
            c_pos_circ = (circle.position[0] - step_size, circle.position[1])
            moving = player1.name
        elif symbol == key.D:
            c_pos_circ = (circle.position[0] + step_size, circle.position[1])
            moving = player1.name
        elif symbol == key.UP:
            c_pos_sqr = (square.position[0], square.position[1] + step_size)
            moving = player2.name
        elif symbol == key.DOWN:
            c_pos_sqr = (square.position[0], square.position[1] - step_size)
            moving = player2.name
        elif symbol == key.LEFT:
            c_pos_sqr = (square.position[0] - step_size, square.position[1])
            moving = player2.name
        elif symbol == key.RIGHT:
            c_pos_sqr = (square.position[0] + step_size, square.position[1])
            moving = player2.name
        elif symbol == key.O:
            print(f'DEBUG: pos square:{c_pos_sqr} pos circle: {c_pos_circ}')
            debug = collision(circle.position, player1.size, square.position, player2.size)
            square_shadow.position = tuple(debug[1])

        if valid_move(c_pos_circ, player1.size, 'radius', win_dim, offset):
            circle.position = c_pos_circ
        if valid_move(c_pos_sqr, player2.size, 'quadrilateral', win_dim, offset):
            square.position = c_pos_sqr

        if collision(circle.position, player1.size, square.position, player2.size)[0]:
            circle.position = player1.position
            square.position = player2.position
            square_shadow.position = player2.position
            score[moving] += 1
            point = moving
            label = pyglet.text.Label(f'SCORE: {score[player1.name]} | {score[player2.name]}',
                                      font_name='Super Legend Boy', font_size=20, x=win_dim[0] / 2 - 120,
                                      y=win_dim[1] - 50)

        if symbol == key.SPACE:
            score[player1.name] = 0
            score[player2.name] = 0
            label = pyglet.text.Label(f'SCORE: {score[player1.name]} | {score[player2.name]}',
                                      font_name='Super Legend Boy', font_size=20, x=win_dim[0] / 2 - 120,
                                      y=win_dim[1] - 50)
            circle.position = player1.position
            square.position = player2.position
            player.queue(battle_music)
            player.next_source()
            square_shadow.position = player2.position

    @window.event
    def on_draw():
        global point
        window.clear()
        BG_.draw()
        batch.draw()
        label.draw()
        if point == player1.name:
            kill1_sound.play()
            point = False
        elif point == player2.name:
            kill2_sound.play()
            point = False

    pyglet.app.run()


if __name__ == "__main__":
    main()
