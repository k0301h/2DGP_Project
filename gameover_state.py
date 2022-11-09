from pico2d import *
import play_state
from monsterclass import monster_place
import game_framework
from map_floor import WIDTH, HEIGHT, ROUND


image0 = None
image1 = None
image2 = None

running = True
timer = 0

def enter():
    print('enter title_state')
    global image0, image1, image2
    image0 = load_image('./Textures/base_skynight.png')
    image1 = load_image('./Textures/journal_back.png')
    image2 = load_image('./Textures/journal_top_gameover.png')

    play_state.main_character.camera_move_x += (play_state.main_character.X - play_state.main_character.camera_move_x - WIDTH // 4)
    print(play_state.main_character.camera_move_y, (play_state.main_character.Y - play_state.main_character.camera_move_y - HEIGHT * 2 // 3))
    play_state.main_character.camera_move_y += (play_state.main_character.Y - play_state.main_character.camera_move_y - HEIGHT * 2 // 3)
    print(play_state.main_character.camera_move_y)

def exit():
    print('exit title_state')
    global image0, image1, image2

    del image0
    del image1
    del image2

    play_state.main_character.Place()
    play_state.main_character.Stun_state = False
    # monster
    play_state.count = 0
    if ROUND >= 1:
        for play_state.monster in play_state.monster_list:
            play_state.monster.Place(monster_place[play_state.count][0], monster_place[play_state.count][1])
            play_state.count += 1


def update():
    # play_state.main_character.camera_move_x = clamp(200, play_state.main_character.X - play_state.main_character.camera_move_x, 300 )
    # print(play_state.main_character.X - play_state.main_character.camera_move_x)

    # global timer, running
    # if timer > 5.0:
    #     timer = 0
    #     running = False
    #     game_framework.change_state(title_state)
    # delay(0.01)
    # timer += 0.01
    pass


def draw():
    pico2d.clear_canvas()
    play_state.draw_world()
    image0.clip_draw(0, 0, 512, 512, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT * 3 / 2)
    image1.clip_draw(0, 0, 2048, 1024, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    image2.clip_draw(0, 0, 2048, 1024, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    pico2d.update_canvas()

def handle_events():
    handle = get_events()
    for event in handle:
        if event.type == SDL_QUIT:
            close_canvas()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                close_canvas()
            elif event.key == SDLK_RETURN:
                # game_framework.change_state(play_state)
                game_framework.pop_state()

def pause(): pass

def resume(): pass