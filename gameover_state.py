from pico2d import *
import play_state
from monsterclass import monster_place
import game_framework
from map_floor import WIDTH, HEIGHT, ROUND


image0 = None
image1 = None
image2 = None

font = None

running = True
timer = 0

def enter():
    print('enter title_state')
    global image0, image1, image2, font
    image0 = load_image('./Textures/base_skynight2.png')
    image1 = load_image('./Textures/journal_back.png')
    image2 = load_image('./Textures/journal_top_gameover.png')

    font = load_font('./Textures/ENCR10B.TTF', 50)

    play_state.main_character.camera_move_x += (play_state.main_character.X - play_state.main_character.camera_move_x - WIDTH // 4)
    # print(play_state.main_character.camera_move_y, (play_state.main_character.Y - play_state.main_character.camera_move_y - HEIGHT * 2 // 3))
    play_state.main_character.camera_move_y += (play_state.main_character.Y - play_state.main_character.camera_move_y - HEIGHT * 2 // 3)
    # print(play_state.main_character.camera_move_y)

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
    pass


def draw():
    pico2d.clear_canvas()
    play_state.draw_world()
    image0.clip_draw(0, 0, 512, 512, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT * 3 / 2)
    image1.clip_draw(0, 0, 2048, 1024, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    image2.clip_draw(0, 0, 2048, 1024, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)

    font.draw(WIDTH * 3 / 5, HEIGHT * 6 / 7, 'You are die!', (255, 255, 255))
    font.draw(WIDTH * 1 / 5, HEIGHT * 1 / 5, ' d__(O > O)__b ', (0, 0, 0))
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