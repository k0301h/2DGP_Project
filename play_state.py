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
UI = None
UI_count = None
monster_list = []
monster_list_1 = [Snake() for i in range(27)]
monster_list_2 = [Bat() for i in range(5)]
# monster_list_3 = [Horned_Lizard for i in range(3)]

monster_place = [[17, 2], [40, 1], [38, 7], [18, 16], [10, 17], [38, 12], [33, 18], [40, 15],
                 [8, 17], [22, 23], [29, 21], [29, 24], [39, 26], [11, 30], [17, 28], [4, 41],
                 [5, 44], [13, 47], [18, 46], [27, 44], [32, 46], [26, 44], [31, 45], [32, 47],
                 [43, 48], [43, 33], [46, 39]]

monster_list += monster_list_1
def enter():
    global main_character, character_I, character_reverse_I, BG_stage_I, FLOOR_stage_I, \
        test_monster, test_monster_image, main_character_grid, test_monster_grid,\
        test_monster_reverse_image, UI, UI_count

    # character
    main_character = CHARACTER()
    main_character.Place()
    # monster
    # test_monster = Snake()
    # test_monster_image = load_image('./Textures/Entities/Monsters/snake.png')
    # test_monster_reverse_image = load_image('./Textures/Entities/Monsters/snake.png')
    count = 0
    for monster in monster_list:
        monster.Place(monster_place[count][0], monster_place[count][1])
        count += 1
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
    #UI
    UI = load_image('./Textures/hud.png')
    UI_count = load_image('./Textures/number.png')

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

    del UI
    del UI_count

def update():
    for monster in monster_list:
        # main_character.Motion(monster)
        monster.Motion(main_character)
    main_character.Motion(monster_list)
    # test_monster.Motion()

def draw():
    pico2d.clear_canvas()
    draw_map_floor(BG_stage_I, FLOOR_stage_I, main_character)
    main_character.draw_character(character_I, character_reverse_I, main_character_grid)
    for monster in monster_list:
        if monster.HP > 0:
            monster.draw_monster(main_character)
        # test_monster.draw_monster(main_character, test_monster_grid)
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