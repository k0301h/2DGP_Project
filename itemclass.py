from pico2d import *
from map_floor import HEIGHT

class bullet:
    X = 0
    Y = 0

class shotgun:
    ATK = 2
    Action = 0
    X = 0
    Y = 0
    image = None

    def __init__(self):
        if shotgun.image == None:
            shotgun.image = load_image('./Textures/items.png')

    def draw(self, character):
        if character.DIRECTION:
            self.image.clip_composite_draw(10, 2048 - 475, 120, 45, 0, 'h', character.X - character.camera_move_x - 17,
                                          character.Y - character.camera_move_y - 12, 40, 15)
        else:
            self.image.clip_composite_draw(10, 2048 - 475, 120, 45, 0, '', character.X - character.camera_move_x + 17,
                                          character.Y - character.camera_move_y - 12, 40, 15)