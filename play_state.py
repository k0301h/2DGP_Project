from pico2d import *

import game_world
import game_framework

import play_state
import gameover_state
import title_state
import stageclear_state

import drawscreen
from characterclass import *
from monsterclass import *

from trap import *
from itemclass import *

main_character = None
BG_stage_I = None
Deco_tutorial_I = None
FLOOR_stage_I = None
trap = None
UI = None
UI_count = None

timer = 0

def enter():
    print("enter play_state")
    global main_character, BG_stage_I, FLOOR_stage_I, UI, UI_count, Deco_tutorial_I, trap

    drawscreen.map_chanege()
    
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
    trap = [Arrow_Trap() for _ in range(2)]
    for count in range(2):
        trap[count].Place(count)
    #UI
    UI = load_image('./Textures/hud.png')
    UI_count = load_image('./Textures/number.png')

    game_world.add_object(main_character, 2)
    game_world.add_objects(monster_list, 2)

    # count = 0
    # for unit in game_world.all_object():
    #     print(unit)
    #     count += 1
    # print(count)
def exit():
    print('exit play_state')
    global main_character, BG_stage_I, FLOOR_stage_I, UI, UI_count, trap, Deco_tutorial_I
    game_world.clear()

    del main_character

    del Deco_tutorial_I
    del BG_stage_I
    del FLOOR_stage_I
    del trap

    del UI
    del UI_count

def update():
    global timer
    # print('update play_state')
    if ROUND >= 1:
        for unit in game_world.all_object():
            if type(unit).__name__ == 'Snake' or type(unit).__name__ == 'Bat' or type(unit).__name__ == 'Horned_Lizard':
                if unit.HP <= 0:
                    game_world.remove_object(unit)
                else:
                    unit.Motion(main_character)

    main_character.Motion(monster_list)

    for count in range(2):
        if not trap[count].attack_state:
            for unit in game_world.all_object():
                trap[count].Attack_boundary(unit)
        else:
            trap[count].Attack_move()

    if main_character.HP <= 0:
        timer += game_framework.frame_time
    elif main_character.scale == 60:
        drawscreen.clear = True
        drawscreen.ROUND += 1
        drawscreen.map_chanege()
        game_framework.change_state(stageclear_state)

    if timer >= 3:
        timer = 0
        main_character.HP = 5
        game_framework.push_state(gameover_state)

def draw_world():
    drawscreen.draw_background(BG_stage_I, main_character)
    drawscreen.draw_map_floor(FLOOR_stage_I, Deco_tutorial_I, trap, main_character, main_character.X -main_character.camera_move_x - WIDTH, main_character.X - main_character.camera_move_x + WIDTH, main_character.Y - HEIGHT, main_character.Y + HEIGHT)  # depth == 2 // main_character.X -main_character.camera_move_x - WIDTH, main_character.X - main_character.camera_move_x + WIDTH, main_character.Y - HEIGHT, main_character.Y + HEIGHT
    main_character.draw()

    if ROUND >= 1:
        for unit in game_world.all_object():
            if type(unit).__name__ == 'CHARACTER':
                unit.draw()
            elif type(unit).__name__ == 'Snake' or type(unit).__name__ == 'Bat' or type(unit).__name__ == 'Horned_Lizard':
                unit.draw_monster(main_character)

    for count in range(2):
        if trap[count].attack_state:
            trap[count].draw(main_character)

    main_character.draw_UI(UI, UI_count)
    # if mode == 1:
    # delay(0.015)

def draw():
    # print('draw play_state')
    pico2d.clear_canvas()
    draw_world()
    pico2d.update_canvas()

def handle_events():
    handle = get_events()
    main_character.handle = handle
    for event in handle:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
    main_character.key_down()

def pause(): pass

def resume(): game_framework.change_state(title_state)