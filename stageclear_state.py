from pico2d import *
from play_state import *

from characterclass import *
import game_framework
import drawscreen

main_character = None
BG_stage_I = None
FLOOR_stage_I = None
BG_stage_I = None

def enter():
    import play_state
    global main_character, BG_stage_I, FLOOR_stage_I
    print('enter stageclear_state')

    main_character = CHARACTER()
    main_character.Place()

    if 1 <= play_state.round_check <= 2:
        BG_stage_I = load_image('./Textures/bg_cave.png')
    elif 3 <= play_state.round_check <= 4:
        BG_stage_I = load_image('./Textures/bg_jungle.png')

    if 1 <= play_state.round_check <= 2:
        FLOOR_stage_I = load_image('./Textures/floor_cave.png')
    elif 3 <= play_state.round_check <= 4:
        FLOOR_stage_I = load_image('./Textures/floor_jungle.png')


def exit():
    global main_character, BG_stage_I, FLOOR_stage_I
    print('exit stageclear_state')

    del main_character

    del BG_stage_I
    del FLOOR_stage_I

def update():
    # print('update stageclear_state')
    main_character.clear_motion()
    # print(main_character.timer)
    if main_character.timer < 1.6:
        main_character.Motion(None)

def draw():
    # print('draw stageclear_state')
    pico2d.clear_canvas()
    drawscreen.draw_background(BG_stage_I, main_character)
    drawscreen.draw_map_floor(FLOOR_stage_I, None, None, main_character,
                   main_character.X - main_character.camera_move_x - WIDTH,
                   main_character.X - main_character.camera_move_x + WIDTH, main_character.Y - HEIGHT,
                   main_character.Y + HEIGHT)  # depth == 2 // main_character.X -main_character.camera_move_x - WIDTH, main_character.X - main_character.camera_move_x + WIDTH, main_character.Y - HEIGHT, main_character.Y + HEIGHT
    main_character.draw()
    pico2d.update_canvas()

def handle_events():
    handle = get_events()
    for event in handle:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                drawscreen.clear = False
                drawscreen.map_chanege()
                game_framework.change_state(play_state)
            elif event.key == SDLK_UP:
                pass
            elif event.key == SDLK_DOWN:
                pass
            elif event.key == SDLK_SPACE:
                pass

def pause(): pass

def resume(): pass