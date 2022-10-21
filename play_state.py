import pico2d
from pico2d import *
from drawscreen import *
from characterclass import *
from monsterclass import *

main_character = None
test_monster = None
character_I = None
character_reverse_I = None
main_character_grid = None
BG_stage_I = None
FLOOR_stage_I = None
test_monster_image = None
test_monster_reverse_image = None
test_monster_grid = None

def enter():
    global main_character, character_I, character_reverse_I, BG_stage_I, FLOOR_stage_I, \
        test_monster, test_monster_image, main_character_grid, test_monster_grid,\
        test_monster_reverse_image

    # character
    main_character = CHARACTER()
    main_character.Place()
    # monster
    test_monster = MONSTER()
    test_monster.Place()
    # character image
    character_I = load_image('./Textures/char_yellow.png')
    character_reverse_I = load_image('./Textures/r_char_yellow.png')
    main_character_grid = load_image('./Textures/Entities/char_yellow_full_grid.png')
    # monster image
    test_monster_image = load_image('./Textures/Entities/Monsters/snake.png')
    test_monster_reverse_image = load_image('./Textures/Entities/Monsters/snake_reverse.png')
    test_monster_grid = load_image('./Textures/Entities/Monsters/snake_grid.png')
    # stage image
    BG_stage_I = load_image('./Textures/bg_cave.png')
    FLOOR_stage_I = load_image('./Textures/floor_cave.png')

def exit():
    del main_character
    del character_I
    del character_reverse_I
    del main_character_grid

    del test_monster
    del test_monster_image
    del test_monster_reverse_image
    del test_monster_grid

    del BG_stage_I
    del FLOOR_stage_I

def update():
    main_character.key_down()
    main_character.Motion(test_monster)
    test_monster.Motion()

def draw():
    pico2d.clear_canvas()
    draw_map_floor(BG_stage_I, FLOOR_stage_I, main_character)
    main_character.draw_character(character_I, character_reverse_I, main_character_grid)
    test_monster.draw_monster(main_character, test_monster_image, test_monster_reverse_image, test_monster_grid)
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