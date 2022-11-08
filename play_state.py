from pico2d import *
from drawscreen import *
from characterclass import *
from monsterclass import *

main_character = None
BG_stage_I = None
Deco_tutorial_I = None
FLOOR_stage_I = None
UI = None
UI_count = None

def enter():
    print("enter play_state")
    global main_character, BG_stage_I, FLOOR_stage_I, UI, UI_count, Deco_tutorial_I

    # character
    main_character = CHARACTER()
    main_character.Place()
    # monster
    count = 0
    if ROUND >= 1:
        for monster in monster_list:
            monster.Place(monster_place[count][0], monster_place[count][1])
            count += 1
    # stage image
    BG_stage_I = load_image('./Textures/bg_cave.png')
    FLOOR_stage_I = load_image('./Textures/floor_cave.png')
    Deco_tutorial_I = load_image('./Textures/deco_tutorial.png')
    #UI
    UI = load_image('./Textures/hud.png')
    UI_count = load_image('./Textures/number.png')

def exit():
    print('exit play_state')
    global main_character, BG_stage_I, FLOOR_stage_I, UI, UI_count

    del main_character

    del BG_stage_I
    del FLOOR_stage_I

    del UI
    del UI_count

def update():
    print('update play_state')
    if ROUND >= 1:
        for monster in monster_list:
            monster.Motion(main_character)

    main_character.Motion(monster_list)

def draw():
    print('draw play_state')
    pico2d.clear_canvas()
    draw_map_floor(BG_stage_I, FLOOR_stage_I, Deco_tutorial_I, main_character)       # depth == 2
    main_character.draw()
    if ROUND >= 1:
        for monster in monster_list:
            if monster.HP > 0:
                monster.draw_monster(main_character)
    main_character.draw_UI(UI, UI_count)
    # delay(0.015)
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