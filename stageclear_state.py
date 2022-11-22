from pico2d import *
from play_state import *

from characterclass import *
import game_framework
from map_floor import *
from drawscreen import *
from trap import *

PIXEL_PER_METER = (10 / 0.5)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

main_character = None
BG_stage_I = None
FLOOR_stage_I = None
trap = None

def enter():
    global main_character, BG_stage_I, FLOOR_stage_I, trap
    print('enter stageclear_state')

    main_character = CHARACTER()
    main_character.Place()

    BG_stage_I = load_image('./Textures/bg_cave.png')
    FLOOR_stage_I = load_image('./Textures/floor_cave.png')
    trap = Arrow_Trap()
    trap.Place(1)


def exit():
    global main_character, BG_stage_I, FLOOR_stage_I, trap
    print('exit stageclear_state')

    del main_character

    del BG_stage_I
    del FLOOR_stage_I
    del trap

def update():
    # print('update stageclear_state')
    pass

def draw():
    # print('draw stageclear_state')
    pico2d.clear_canvas()
    draw_map_floor(FLOOR_stage_I, None, trap, main_character,
                   main_character.X - main_character.camera_move_x - WIDTH,
                   main_character.X - main_character.camera_move_x + WIDTH, main_character.Y - HEIGHT,
                   main_character.Y + HEIGHT)  # depth == 2 // main_character.X -main_character.camera_move_x - WIDTH, main_character.X - main_character.camera_move_x + WIDTH, main_character.Y - HEIGHT, main_character.Y + HEIGHT
    pico2d.update_canvas()

def handle_events():
    global clear
    handle = get_events()
    for event in handle:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                clear = False
                map_chanege()
                game_framework.change_state(play_state)
            elif event.key == SDLK_UP:
                pass
            elif event.key == SDLK_DOWN:
                pass
            elif event.key == SDLK_SPACE:
                pass

def pause(): pass

def resume(): pass