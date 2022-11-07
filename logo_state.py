from pico2d import *
import title_state

import game_framework
from map_floor import WIDTH, HEIGHT

image1 = None
image2 = None

running = True
timer = 0

def enter():
    print('enter title_state')
    global image1, image2
    image1 = load_image('./Textures/splash0.png')
    image2 = load_image('./Textures/splash1.png')

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
        game_framework.change_state(title_state)
    delay(0.01)
    timer += 0.01


def draw():
    pico2d.clear_canvas()
    if timer <= 2.5:
        image1.clip_draw(0, 0, 1920, 1080, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    else:
        image2.clip_draw(0, 0, 1920, 1080, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    pico2d.update_canvas()

def handle_events():
    handle = get_events()
    for event in handle:
        if event.type == SDL_QUIT:
            close_canvas()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                close_canvas()

def pause(): pass

def resume(): pass