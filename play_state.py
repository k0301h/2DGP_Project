import pico2d
from pico2d import *
from drawscreen import *
from characterclass import *

main_character = None
character_I = None
character_reverse_I = None
BG_stage_I = None
FLOOR_stage_I = None

def enter():
    global main_character, character_I, character_reverse_I, BG_stage_I, FLOOR_stage_I
    main_character = CHARACTER()
    main_character.Place()
    character_I = load_image('char_yellow.png')
    character_reverse_I = load_image('./Textures/r_char_yellow.png')
    BG_stage_I = load_image('./Textures/bg_cave.png')
    FLOOR_stage_I = load_image('./Textures/floor_cave.png')

def exit():
    del main_character
    del character_I
    del character_reverse_I
    del BG_stage_I
    del FLOOR_stage_I

def update():
    main_character.key_down()
    main_character.Motion()

def draw():
    pico2d.clear_canvas()
    draw_map_floor(BG_stage_I, FLOOR_stage_I, main_character)
    main_character.draw_character(character_I, character_reverse_I)
    main_character.draw_UI()
    pico2d.update_canvas()

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            close_canvas()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                close_canvas()

def pause(): pass

def resume(): pass