from pico2d import *
from drawscreen import *
from characterclass import *
from monsterclass import *
import gameover_state
import game_framework

main_character = None
BG_stage_I = None
Deco_tutorial_I = None
FLOOR_stage_I = None
trap_I = None
UI = None
UI_count = None

timer = 0

def enter():
    print("enter play_state")
    global main_character, BG_stage_I, FLOOR_stage_I, UI, UI_count, Deco_tutorial_I, trap_I

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
    trap_I = load_image('./Textures/journal_entry_traps.png')
    #UI
    UI = load_image('./Textures/hud.png')
    UI_count = load_image('./Textures/number.png')

def exit():
    print('exit play_state')
    global main_character, BG_stage_I, FLOOR_stage_I, UI, UI_count, trap_I, Deco_tutorial_I

    del main_character

    del Deco_tutorial_I
    del BG_stage_I
    del FLOOR_stage_I
    del trap_I

    del UI
    del UI_count

def update():
    global timer
    # print('update play_state')
    if ROUND >= 1:
        for monster in monster_list:
            if monster.HP <= 0:
                monster_list.remove(monster)
                del monster
            else:
                monster.Motion(main_character)
    main_character.Motion(monster_list)

    if main_character.HP <= 0:
        timer += 0.05
        delay(0.01)
    if timer >= 3:
        timer = 0
        main_character.HP = 5
        # game_framework.change_state(gameover_state)
        game_framework.push_state(gameover_state)

def draw_world():
    draw_map_floor(BG_stage_I, FLOOR_stage_I, Deco_tutorial_I, trap_I, main_character, main_character.X -main_character.camera_move_x - WIDTH, main_character.X - main_character.camera_move_x + WIDTH, main_character.Y - HEIGHT, main_character.Y + HEIGHT)  # depth == 2
    print(main_character.Y - HEIGHT, main_character.Y + HEIGHT)
    main_character.draw()
    if ROUND >= 1:
        for monster in monster_list:
            if monster.HP > 0:
                monster.draw_monster(main_character)
    main_character.draw_UI(UI, UI_count)
    if mode == 1:
        delay(0.015)

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

def resume(): pass