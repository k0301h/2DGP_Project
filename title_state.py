from pico2d import *
import play_state

import game_framework
from map_floor import WIDTH, HEIGHT

image1 = None
image2 = None

running = True
timer = 0

def enter():
    print('enter title_state')
    global image1, image2
    image1 = load_image('./Textures/menu_title.png')
    image2 = load_image('./Textures/menu_titlegal.png')

def exit():
    print('exit title_state')
    global image1, image2
    del image1
    del image2


def update():
    global timer, running
    if timer > 5.0:
        timer = 0
        running = False
        game_framework.change_state(play_state)
    delay(0.01)
    timer += 0.01


def draw():
    pico2d.clear_canvas()
    image1.clip_draw(0, 0,1920, 1080, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    image2.clip_draw(0, 0, 1024, 1024, WIDTH / 3, HEIGHT / 3, HEIGHT, HEIGHT)
    pico2d.update_canvas()

def handle_events():
    pass

def pause(): pass

def resume(): pass