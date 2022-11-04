import pico2d
from pico2d import *
from drawscreen import *
from characterclass import *
from monsterclass import *

main_character = None
BG_stage_I = None
FLOOR_stage_I = None
UI = None
UI_count = None

def enter():
    global main_character, BG_stage_I, FLOOR_stage_I, UI, UI_count

    # character
    main_character = CHARACTER()
    main_character.Place()
    # monster
    count = 0
    for monster in monster_list:
        print(monster_place[count])
        monster.Place(monster_place[count][0], monster_place[count][1])
        count += 1
    # stage image
    BG_stage_I = load_image('./Textures/bg_cave.png')
    FLOOR_stage_I = load_image('./Textures/floor_cave.png')
    #UI
    UI = load_image('./Textures/hud.png')
    UI_count = load_image('./Textures/number.png')

def exit():
    del main_character

    del BG_stage_I
    del FLOOR_stage_I

    del UI
    del UI_count

def update():
    for monster in monster_list:
        monster.Motion(main_character)
    main_character.Motion(monster_list)

def draw():
    pico2d.clear_canvas()
    draw_map_floor(BG_stage_I, FLOOR_stage_I, main_character)       # depth == 2
    main_character.draw()
    for monster in monster_list:
        if monster.HP > 0:
            monster.draw_monster(main_character)
    main_character.draw_UI(UI, UI_count)
    pico2d.update_canvas()

def handle_events():
    handle = get_events()
    main_character.handle = handle
    for event in handle:
        if event.type == SDL_QUIT:
            close_canvas()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                close_canvas()
    main_character.key_down()

def pause(): pass

def resume(): pass